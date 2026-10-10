"""Tests de «¿se repite?», comparación predictiva y regla de decisión."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .pitagoras import ajustar_k_tabla, pitagorico

NIVEL_IC = (5, 95)  # IC90%
ALFA = 0.10


def desvio(t: pd.DataFrame, k: float) -> pd.Series:
    """Victorias reales − G·pitagórico."""
    return t["V"] - t["G"] * pitagorico(t["PF"], t["PC"], k)


def _pearson(x: np.ndarray, y: np.ndarray) -> float:
    return float(np.corrcoef(x, y)[0, 1])


def contraste_mitades(d1: pd.Series, d2: pd.Series, n: int, rng: np.random.Generator) -> dict:
    """Test A: correlación entre el desvío de la 1ª y la 2ª vuelta; IC por bootstrap de equipos."""
    x, y = d1.to_numpy(), d2.to_numpy()
    r = _pearson(x, y)
    rs = []
    while len(rs) < n:
        i = rng.integers(0, len(x), len(x))
        if x[i].std() > 0 and y[i].std() > 0:
            rs.append(_pearson(x[i], y[i]))
    lo, hi = np.percentile(rs, NIVEL_IC)
    return {"r": r, "ic90_bajo": float(lo), "ic90_alto": float(hi)}


def _rms(d: np.ndarray, axis=None) -> np.ndarray | float:
    return np.sqrt(np.mean(np.square(d), axis=axis))


def contraste_varianza(desvio_obs: pd.Series, esperadas: pd.Series, wins_sim: pd.DataFrame) -> dict:
    """Test B: dispersión (RMS) de desvíos observada vs la de temporadas simuladas por azar."""
    obs = float(_rms(desvio_obs.to_numpy()))
    sim = _rms(wins_sim[esperadas.index].to_numpy() - esperadas.to_numpy(), axis=1)
    return {
        "rms_observado": obs,
        "rms_azar_mediana": float(np.median(sim)),
        "rms_azar_p95": float(np.percentile(sim, 95)),
        "p_valor": float(np.mean(sim >= obs)),
    }


def decision(a: dict, b: dict) -> dict:
    """Regla pre-registrada: señal solo si IC90% de A excluye 0 por arriba Y p de B < 0,10."""
    cond_a = a["ic90_bajo"] > 0
    cond_b = b["p_valor"] < ALFA
    return {
        "cond_a": bool(cond_a),
        "cond_b": bool(cond_b),
        "conclusion": "senal_de_habilidad" if cond_a and cond_b else "compatible_con_azar",
    }


def comparacion_predictiva(t1: pd.DataFrame, t2: pd.DataFrame, n: int, rng) -> dict:
    """Correlación con el % de victorias de la 2ª vuelta de tres predictores de la 1ª vuelta."""
    k1 = ajustar_k_tabla(t1)  # k solo con la 1ª vuelta, para no filtrar información
    pred = {
        "pct_victorias": t1["pct_v"].to_numpy(),
        "pct_pitagorico": pitagorico(t1["PF"], t1["PC"], k1),
        "net_rtg": t1["net_rtg"].to_numpy(),
    }
    y = t2["pct_v"].to_numpy()
    r = {nombre: _pearson(x, y) for nombre, x in pred.items()}
    pares = [("pct_pitagorico", "pct_victorias"), ("net_rtg", "pct_victorias"),
             ("net_rtg", "pct_pitagorico")]  # fmt: skip
    difs = {p: [] for p in pares}
    for _ in range(n):
        i = rng.integers(0, len(y), len(y))
        if y[i].std() == 0 or any(x[i].std() == 0 for x in pred.values()):
            continue
        rb = {nombre: _pearson(x[i], y[i]) for nombre, x in pred.items()}
        for a, b in pares:
            difs[(a, b)].append(rb[a] - rb[b])
    out = {"k_vuelta1": k1, "r": r, "diferencias": {}}
    for (a, b), v in difs.items():
        lo, hi = np.percentile(v, NIVEL_IC)
        out["diferencias"][f"{a}_menos_{b}"] = {
            "dif": r[a] - r[b], "ic90_bajo": float(lo), "ic90_alto": float(hi)
        }  # fmt: skip
    return out
