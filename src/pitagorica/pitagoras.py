"""Expectativa pitagórica: fórmula, ajuste de k y validación."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar

from . import K_NBA

K_MIN, K_MAX = 1.0, 40.0


def pitagorico(pf, pc, k: float):
    """% de victorias esperado: PF^k / (PF^k + PC^k). Escala por la media para evitar overflow."""
    pf = np.asarray(pf, dtype=float)
    pc = np.asarray(pc, dtype=float)
    m = np.maximum(pf, pc)
    a, b = (pf / m) ** k, (pc / m) ** k
    return a / (a + b)


def ajustar_k(victorias, partidos, pf, pc) -> float:
    """k que minimiza la suma de cuadrados entre % real de victorias y % pitagórico."""
    victorias, partidos = np.asarray(victorias, float), np.asarray(partidos, float)
    real = victorias / partidos

    def sse(k: float) -> float:
        return float(np.sum((real - pitagorico(pf, pc, k)) ** 2))

    return float(minimize_scalar(sse, bounds=(K_MIN, K_MAX), method="bounded").x)


def ajustar_k_tabla(t: pd.DataFrame) -> float:
    return ajustar_k(t["V"], t["G"], t["PF"], t["PC"])


def error_medio(t: pd.DataFrame, k: float) -> float:
    """Error absoluto medio en victorias: media de |V − G·pitagórico|."""
    esperadas = t["G"] * pitagorico(t["PF"], t["PC"], k)
    return float(np.mean(np.abs(t["V"] - esperadas)))


def curva_error(t: pd.DataFrame, ks: np.ndarray) -> np.ndarray:
    return np.array([error_medio(t, k) for k in ks])


def validacion_mitades(t1: pd.DataFrame, t2: pd.DataFrame) -> dict:
    """k ajustado en una vuelta, error medido en la otra (y media de las dos direcciones)."""
    k1, k2 = ajustar_k_tabla(t1), ajustar_k_tabla(t2)
    e_k = np.mean([error_medio(t2, k1), error_medio(t1, k2)])
    e_nba = np.mean([error_medio(t2, K_NBA), error_medio(t1, K_NBA)])
    return {"k_vuelta1": k1, "k_vuelta2": k2, "error_acb": float(e_k), "error_k14": float(e_nba)}


def validacion_loo(t: pd.DataFrame) -> dict:
    """Dejar un equipo fuera: k con 17 equipos, error en el equipo excluido."""
    errs, errs14, ks = [], [], []
    for eq in t.index:
        resto = t.drop(eq)
        k = ajustar_k_tabla(resto)
        ks.append(k)
        errs.append(error_medio(t.loc[[eq]], k))
        errs14.append(error_medio(t.loc[[eq]], K_NBA))
    return {
        "error_acb": float(np.mean(errs)),
        "error_k14": float(np.mean(errs14)),
        "k_min": float(np.min(ks)),
        "k_max": float(np.max(ks)),
    }


def bootstrap_k(df: pd.DataFrame, n: int, rng: np.random.Generator) -> np.ndarray:
    """Bootstrap de partidos: remuestrea los 306 partidos y reajusta k."""
    ids = df["game_id"].unique()
    pos = {g: i for i, g in enumerate(ids)}
    fila_partido = df["game_id"].map(pos).to_numpy()
    equipos = pd.factorize(df["team"])[0]
    n_eq = equipos.max() + 1
    vic, pf, pc = (df[c].to_numpy(float) for c in ("victoria", "pts", "opp_pts"))
    ks = np.empty(n)
    for b in range(n):
        peso = np.bincount(rng.integers(0, len(ids), len(ids)), minlength=len(ids))[fila_partido]
        g = np.bincount(equipos, weights=peso, minlength=n_eq)
        ks[b] = ajustar_k(
            np.bincount(equipos, weights=peso * vic, minlength=n_eq),
            g,
            np.bincount(equipos, weights=peso * pf, minlength=n_eq),
            np.bincount(equipos, weights=peso * pc, minlength=n_eq),
        )
    return ks
