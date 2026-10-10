"""Figuras del artículo (paleta Basketmática: tinta, papel y teja)."""

from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.figure import Figure

from . import K_NBA
from .datos import NOMBRE_CORTO

INK, PAPER, RULE = "#1A1A1A", "#FAF8F3", "#D9D4C7"
TEJA, TEJA_TXT = "#C8853A", "#98642A"
POS, NEG = "#4A7C59", "#A0392E"
GRIS = "#6B6B6B"


def estilo() -> None:
    mpl.rcParams.update(
        {
            "figure.facecolor": PAPER, "axes.facecolor": PAPER, "savefig.facecolor": PAPER,
            "text.color": INK, "axes.labelcolor": INK, "axes.edgecolor": INK,
            "xtick.color": INK, "ytick.color": INK, "grid.color": RULE,
            "font.family": "sans-serif",
            "font.sans-serif": ["Inter", "IBM Plex Sans", "Helvetica Neue", "Arial", "DejaVu Sans"],
            "axes.spines.top": False, "axes.spines.right": False,
            "axes.titlelocation": "left", "axes.titleweight": "bold", "axes.titlesize": 13,
            "axes.grid": True, "axes.axisbelow": True, "grid.linewidth": 0.5,
            "legend.frameon": False, "savefig.dpi": 200, "savefig.bbox": "tight",
        }
    )  # fmt: skip


def _corto(e: str) -> str:
    return NOMBRE_CORTO.get(e, e)


def fig_curva_k(ks, errores, k_acb: float, ic: tuple[float, float]) -> Figure:
    estilo()
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.axvspan(*ic, color=TEJA, alpha=0.15, lw=0, label="IC90% de k (bootstrap de partidos)")
    ax.plot(ks, errores, color=INK, lw=1.8)
    ax.axvline(K_NBA, color=GRIS, ls="--", lw=1.2)
    ax.axvline(k_acb, color=TEJA, lw=1.8)
    y0 = errores.max()
    ax.text(K_NBA, y0, f" NBA k = {K_NBA:.0f}", color=GRIS, va="top", ha="right")
    ax.text(k_acb, y0, f" ACB k = {k_acb:.1f}", color=TEJA_TXT, va="top", ha="left")
    ax.set_xlabel("Exponente k")
    ax.set_ylabel("Error medio (victorias por equipo)")
    ax.set_title("¿Qué exponente describe mejor la ACB 25/26?")
    ax.legend(loc="lower right")
    return fig


def fig_desvios(t: pd.DataFrame) -> Figure:
    """Barras divergentes del desvío con la banda del azar (90%) sombreada."""
    estilo()
    t = t.sort_values("desvio")
    fig, ax = plt.subplots(figsize=(7, 6))
    y = np.arange(len(t))
    ax.barh(y, t["p_alto"] - t["p_bajo"], left=t["p_bajo"] - t["esperadas"],
            color=RULE, height=0.8, label="Banda del azar (90%)")  # fmt: skip
    colores = np.where(t["desvio"] >= 0, POS, NEG)
    ax.barh(y, t["desvio"], color=colores, height=0.45)
    for yi, (eq, f) in enumerate(t.iterrows()):
        ax.text(f["desvio"] + (0.15 if f["desvio"] >= 0 else -0.15), yi,
                f"{f['desvio']:+.1f}", va="center", fontsize=8,
                ha="left" if f["desvio"] >= 0 else "right")  # fmt: skip
    ax.axvline(0, color=INK, lw=0.8)
    ax.set_yticks(y, [_corto(e) for e in t.index])
    ax.set_xlabel("Victorias reales − victorias esperadas")
    ax.grid(axis="y", visible=False)
    ax.set_title("Quién ganó más (y menos) de lo que decían sus puntos")
    ax.legend(loc="lower right")
    return fig


def fig_mitades(d1: pd.Series, d2: pd.Series, r: float, ic: tuple[float, float]) -> Figure:
    estilo()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.axhline(0, color=INK, lw=0.8)
    ax.axvline(0, color=INK, lw=0.8)
    ax.scatter(d1, d2, color=TEJA, s=40, zorder=3)
    for e in d1.index:
        ax.annotate(
            _corto(e), (d1[e], d2[e]), xytext=(4, 4), textcoords="offset points", fontsize=8
        )
    lim = float(max(d1.abs().max(), d2.abs().max())) + 0.8
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    kw = {"fontsize": 8, "color": GRIS}
    ax.text(lim * 0.97, lim * 0.95, "Por encima las dos vueltas", ha="right", va="top", **kw)
    ax.text(-lim * 0.97, -lim * 0.95, "Por debajo las dos vueltas", ha="left", va="bottom", **kw)
    ax.text(-lim * 0.97, lim * 0.95, "Corrige al alza", ha="left", va="top", **kw)
    ax.text(lim * 0.97, -lim * 0.95, "Corrige a la baja", ha="right", va="bottom", **kw)
    ax.set_xlabel("Desvío 1ª vuelta (J1-17)")
    ax.set_ylabel("Desvío 2ª vuelta (J18-34)")
    ax.set_title(f"¿Se repite? r = {r:.2f} (IC90% {ic[0]:.2f} a {ic[1]:.2f})")
    return fig


def fig_prediccion(res: dict) -> Figure:
    estilo()
    nombres = {
        "pct_victorias": "% victorias",
        "pct_pitagorico": "% pitagórico",
        "net_rtg": "NetRtg",
    }
    fig, ax = plt.subplots(figsize=(6, 3.6))
    claves = list(nombres)
    ax.bar(range(3), [res["r"][c] for c in claves], color=[GRIS, TEJA, INK], width=0.55)
    for i, c in enumerate(claves):
        ax.text(i, res["r"][c] + 0.015, f"{res['r'][c]:.2f}", ha="center", fontsize=9)
    ax.set_xticks(range(3), [nombres[c] for c in claves])
    ax.set_ylim(0, 1)
    ax.set_ylabel("r con el % de victorias de la 2ª vuelta")
    ax.grid(axis="x", visible=False)
    ax.set_title("¿Qué de la 1ª vuelta predice mejor la 2ª?")
    return fig
