"""Simulación partido a partido sobre el calendario real (log5 + ventaja de campo)."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import brentq


def prob_local(s_local: np.ndarray, s_visit: np.ndarray, h: float) -> np.ndarray:
    """P(gana el local): log5 con multiplicador de odds h por jugar en casa."""
    o_l = s_local / (1 - s_local)
    o_v = s_visit / (1 - s_visit)
    return o_l * h / (o_l * h + o_v)


def calibrar_h(s_local: np.ndarray, s_visit: np.ndarray, victorias_locales: int) -> float:
    """h tal que la suma de probabilidades locales iguala las victorias locales observadas."""
    return float(
        brentq(lambda h: prob_local(s_local, s_visit, h).sum() - victorias_locales, 0.2, 10.0)
    )


def simular(
    cal: pd.DataFrame, fuerza: pd.Series, n: int, rng: np.random.Generator
) -> tuple[pd.DataFrame, dict]:
    """Simula n temporadas. Devuelve victorias simuladas (n × equipos) y diagnóstico."""
    equipos = list(fuerza.index)
    idx = {e: i for i, e in enumerate(equipos)}
    loc = cal["local"].map(idx).to_numpy()
    vis = cal["visitante"].map(idx).to_numpy()
    s = fuerza.to_numpy()
    victorias_locales = int((cal["pts_local"] > cal["pts_visit"]).sum())
    h = calibrar_h(s[loc], s[vis], victorias_locales)
    p = prob_local(s[loc], s[vis], h)
    n_part, n_eq = len(cal), len(equipos)
    M_loc = np.zeros((n_part, n_eq))
    M_vis = np.zeros((n_part, n_eq))
    M_loc[np.arange(n_part), loc] = 1
    M_vis[np.arange(n_part), vis] = 1
    gana_local = (rng.random((n, n_part)) < p).astype(float)
    wins = gana_local @ M_loc + (1 - gana_local) @ M_vis
    esperadas = p @ M_loc + (1 - p) @ M_vis
    diag = {
        "h": h,
        "pct_local_observado": victorias_locales / n_part,
        "esperadas_log5": pd.Series(esperadas, index=equipos),
    }
    return pd.DataFrame(wins, columns=equipos), diag


def banda(wins_sim: pd.DataFrame, lo: float = 5, hi: float = 95) -> pd.DataFrame:
    return pd.DataFrame(
        {"p_bajo": wins_sim.quantile(lo / 100), "p_alto": wins_sim.quantile(hi / 100)}
    )
