"""Análisis con varias temporadas: k fuera de muestra y persistencia del desvío (t → t+1)."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np
import pandas as pd

from . import K_NBA
from .datos import TRANSICIONES
from .pitagoras import ajustar_k, pitagorico

NIVEL_IC = (5, 95)  # IC90%
PARTIDOS_REF = 34  # los desvíos y errores se expresan por 34 partidos


# --- k fuera de muestra ----------------------------------------------------------------------
def k_conjunto(ts: pd.DataFrame) -> float:
    """k que minimiza la suma de cuadrados del % de victorias sobre todos los equipos-temporada."""
    return ajustar_k(ts["V"], ts["G"], ts["PF"], ts["PC"])


def k_sin_temporada(ts: pd.DataFrame) -> dict[str, float]:
    """k_{−s} para cada temporada s: ajustado solo con las demás."""
    return {s: k_conjunto(ts[ts["season"] != s]) for s in sorted(ts["season"].unique())}


def error_medio34(ts: pd.DataFrame, k: float) -> float:
    """Error absoluto medio en victorias por 34 partidos: media de |%V − %pitagórico|·34."""
    return float(np.mean(np.abs(ts["pct_v"] - pitagorico(ts["PF"], ts["PC"], k))) * PARTIDOS_REF)


def validacion_k(ts: pd.DataFrame) -> pd.DataFrame:
    """Por temporada: k_{−s}, k propio y errores con k_{−s}, con k=14 y con k propio."""
    ks = k_sin_temporada(ts)
    filas = []
    for s, g in ts.groupby("season"):
        k_propio = k_conjunto(g)
        filas.append(
            {
                "temporada": s,
                "k_sin_temporada": ks[s],
                "k_propio": k_propio,
                "error_k_sin_temporada": error_medio34(g, ks[s]),
                "error_k14": error_medio34(g, K_NBA),
                "error_k_propio": error_medio34(g, k_propio),
            }
        )
    return pd.DataFrame(filas)


def bootstrap_k_conjunto(df: pd.DataFrame, n: int, rng: np.random.Generator) -> np.ndarray:
    """Bootstrap de partidos dentro de cada temporada; reajusta el k conjunto en cada remuestreo."""
    ts_id = pd.factorize(df["season"] + "|" + df["club"])[0]
    n_ts = ts_id.max() + 1
    # id de partido global y rango de partidos de cada temporada
    pid = pd.factorize(df["season"] + "|" + df["game_id"].astype(str))[0]
    n_part = pid.max() + 1
    rangos = []
    for s in df["season"].unique():
        ids = np.unique(pid[(df["season"] == s).to_numpy()])
        rangos.append((ids.min(), ids.max() + 1))
    vic, pf, pc = (df[c].to_numpy(float) for c in ("victoria", "pts", "opp_pts"))
    ks = np.empty(n)
    for b in range(n):
        cuenta = np.zeros(n_part)
        for a, z in rangos:
            cuenta[a:z] = np.bincount(rng.integers(a, z, z - a) - a, minlength=z - a)
        w = cuenta[pid]
        g = np.bincount(ts_id, weights=w, minlength=n_ts)
        ks[b] = ajustar_k(
            np.bincount(ts_id, weights=w * vic, minlength=n_ts),
            g,
            np.bincount(ts_id, weights=w * pf, minlength=n_ts),
            np.bincount(ts_id, weights=w * pc, minlength=n_ts),
        )
    return ks


# --- desvíos y pares t → t+1 -----------------------------------------------------------------
def con_desvios(ts: pd.DataFrame) -> pd.DataFrame:
    """Añade k_{−s}, %pitagórico, esperadas y desvío (en victorias por 34 partidos)."""
    ks = k_sin_temporada(ts)
    out = ts.copy()
    out["k"] = out["season"].map(ks)
    out["pyth"] = pitagorico(out["PF"], out["PC"], out["k"].to_numpy())
    out["esperadas34"] = out["pyth"] * PARTIDOS_REF
    out["desvio34"] = (out["pct_v"] - out["pyth"]) * PARTIDOS_REF
    return out


def pares(td: pd.DataFrame, transiciones=TRANSICIONES) -> pd.DataFrame:
    """Pares (club en t, mismo club en t+1) de las transiciones indicadas."""
    cols = ["club", "pct_v", "pyth", "net_rtg", "pct_ig", "desvio34"]
    partes = []
    for a, b in transiciones:
        x = td[td["season"] == a][cols]
        y = td[td["season"] == b][cols]
        m = x.merge(y, on="club", suffixes=("_t", "_t1"))
        m.insert(0, "temporada_t1", b)
        m.insert(0, "temporada_t", a)
        partes.append(m)
    return pd.concat(partes, ignore_index=True)


def _r(x: np.ndarray, y: np.ndarray) -> float:
    return float(np.corrcoef(x, y)[0, 1])


def _pendiente(x: np.ndarray, y: np.ndarray) -> float:
    return float(np.cov(x, y, ddof=1)[0, 1] / np.var(x, ddof=1))


def bootstrap_clubes(
    p: pd.DataFrame,
    estadisticos: dict[str, Callable[[pd.DataFrame], float]],
    n: int,
    rng: np.random.Generator,
) -> dict[str, dict[str, float]]:
    """Bootstrap por clubes: remuestrea franquicias enteras con todos sus pares."""
    grupos = [g for _, g in p.groupby("club")]
    est = {k: f(p) for k, f in estadisticos.items()}
    muestras: dict[str, list[float]] = {k: [] for k in estadisticos}
    for _ in range(n):
        idx = rng.integers(0, len(grupos), len(grupos))
        q = pd.concat([grupos[i] for i in idx], ignore_index=True)
        try:
            vals = {k: f(q) for k, f in estadisticos.items()}
        except FloatingPointError:
            continue
        if all(np.isfinite(v) for v in vals.values()):
            for k, v in vals.items():
                muestras[k].append(v)
    out = {}
    for k, v in muestras.items():
        lo, hi = np.percentile(v, NIVEL_IC)
        out[k] = {"estimacion": est[k], "ic90_bajo": float(lo), "ic90_alto": float(hi)}
    return out


def persistencia(p: pd.DataFrame, n: int, rng: np.random.Generator) -> dict:
    """Test principal: r y pendiente del desvío de t frente al de t+1, IC90% por clubes."""
    est = {
        "r": lambda q: _r(q["desvio34_t"].to_numpy(), q["desvio34_t1"].to_numpy()),
        "pendiente": lambda q: _pendiente(q["desvio34_t"].to_numpy(), q["desvio34_t1"].to_numpy()),
    }
    res = bootstrap_clubes(p, est, n, rng)
    res["n_pares"] = int(len(p))
    res["r_por_transicion"] = {
        f"{a}->{b}": _r(g["desvio34_t"].to_numpy(), g["desvio34_t1"].to_numpy())
        for (a, b), g in p.groupby(["temporada_t", "temporada_t1"])
    }
    res["conclusion"] = "senal_de_habilidad" if res["r"]["ic90_bajo"] > 0 else "compatible_con_azar"
    return res


def finales(p: pd.DataFrame, n: int, rng: np.random.Generator) -> dict:
    """Secundario: ¿se repite el % de victorias en partidos igualados de t a t+1?"""
    q = p.dropna(subset=["pct_ig_t", "pct_ig_t1"])
    est = {"r": lambda g: _r(g["pct_ig_t"].to_numpy(), g["pct_ig_t1"].to_numpy())}
    return {**bootstrap_clubes(q, est, n, rng), "n_pares": int(len(q))}


def prediccion(p: pd.DataFrame, n: int, rng: np.random.Generator) -> dict:
    """Secundario: qué de t predice mejor el % de victorias de t+1 (con diferencias y su IC)."""
    y = "pct_v_t1"

    def r_de(pred):
        return lambda q: _r(q[pred].to_numpy(), q[y].to_numpy())

    est = {
        "r_pct_victorias": r_de("pct_v_t"),
        "r_pct_pitagorico": r_de("pyth_t"),
        "r_net_rtg": r_de("net_rtg_t"),
    }
    est["dif_pitagorico_menos_victorias"] = lambda q: (
        est["r_pct_pitagorico"](q) - est["r_pct_victorias"](q)
    )
    est["dif_netrtg_menos_victorias"] = lambda q: est["r_net_rtg"](q) - est["r_pct_victorias"](q)
    est["dif_netrtg_menos_pitagorico"] = lambda q: est["r_net_rtg"](q) - est["r_pct_pitagorico"](q)
    return bootstrap_clubes(p, est, n, rng)
