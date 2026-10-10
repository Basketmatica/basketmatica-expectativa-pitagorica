"""Carga del CSV de partidos y agregados por equipo."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

RUTA_CSV = Path(__file__).resolve().parents[2] / "data" / "acb_partidos_2025_26.csv"
JORNADA_CORTE = 17  # 1ª vuelta: jornadas 1-17; 2ª vuelta: 18-34
MARGEN_IGUALADO = 5

NOMBRE_CORTO = {
    "BAXI Manresa": "Manresa",
    "Baskonia": "Baskonia",
    "Bàsquet Girona": "Girona",
    "Casademont Zaragoza": "Zaragoza",
    "Coviran Granada": "Granada",
    "FC Barcelona": "Barça",
    "Gran Canaria": "Gran Canaria",
    "Hiopos Lleida": "Lleida",
    "Joventut": "Joventut",
    "La Laguna Tenerife": "Tenerife",
    "MoraBanc Andorra": "Andorra",
    "Real Madrid": "Real Madrid",
    "Recoletas Salud San Pablo Burgos": "Burgos",
    "Río Breogán": "Breogán",
    "Surne Bilbao Basket": "Bilbao",
    "UCAM Murcia": "Murcia",
    "Unicaja": "Unicaja",
    "Valencia Basket": "Valencia",
}


def cargar(ruta: Path | str = RUTA_CSV) -> pd.DataFrame:
    """Lee el CSV (un registro por equipo-partido) y añade victoria, margen e igualado."""
    df = pd.read_csv(ruta)
    df["margen"] = df["pts"] - df["opp_pts"]
    df["victoria"] = (df["margen"] > 0).astype(int)
    df["igualado"] = (df["margen"].abs() <= MARGEN_IGUALADO) | (df["overtimes"] > 0)
    df["vuelta"] = np.where(df["jornada"] <= JORNADA_CORTE, 1, 2)
    df["posesiones"] = posesiones(df)
    return df


def posesiones(df: pd.DataFrame) -> pd.Series:
    """Posesiones por partido (Oliver): media de la estimación ofensiva y la defensiva."""
    off = df["fg_att"] + 0.44 * df["ft_att"] - df["oreb"] + df["tov"]
    deff = df["opp_fg_att"] + 0.44 * df["opp_ft_att"] - df["opp_oreb"] + df["opp_tov"]
    return (off + deff) / 2


def tabla_equipos(df: pd.DataFrame, vuelta: int | None = None) -> pd.DataFrame:
    """Totales por equipo (G, V, PF, PC, posesiones, NetRtg), opcionalmente de una vuelta."""
    d = df if vuelta is None else df[df["vuelta"] == vuelta]
    t = d.groupby("team").agg(
        G=("victoria", "size"),
        V=("victoria", "sum"),
        PF=("pts", "sum"),
        PC=("opp_pts", "sum"),
        pos=("posesiones", "sum"),
    )
    t["pct_v"] = t["V"] / t["G"]
    t["net_rtg"] = 100 * (t["PF"] - t["PC"]) / t["pos"]
    return t.sort_index()


def partidos(df: pd.DataFrame) -> pd.DataFrame:
    """Un registro por partido, visto desde el local."""
    h = df[df["home_away"] == "home"].rename(columns={"team": "local", "opponent": "visitante"})
    return (
        h[["game_id", "jornada", "local", "visitante", "pts", "opp_pts", "overtimes"]]
        .rename(columns={"pts": "pts_local", "opp_pts": "pts_visit"})
        .reset_index(drop=True)
    )


def balance_igualados(df: pd.DataFrame) -> pd.DataFrame:
    """Victorias y derrotas de cada equipo en partidos igualados y no igualados."""
    g = df.groupby(["team", "igualado"])["victoria"].agg(["sum", "size"]).unstack(fill_value=0)
    out = pd.DataFrame(index=g.index)
    out["V_igualados"] = g[("sum", True)]
    out["D_igualados"] = g[("size", True)] - g[("sum", True)]
    out["V_resto"] = g[("sum", False)]
    out["D_resto"] = g[("size", False)] - g[("sum", False)]
    return out
