"""Deriva el CSV de partidos (un registro por equipo-partido) desde un parquet de boxscores.

Uso (opcional, el CSV ya está versionado en data/):
    python scripts/extraer_partidos.py RUTA_PARQUET data/acb_partidos_2025_26.csv

El parquet es un boxscore por jugador y partido (liga regular ACB). Solo se
conservan totales de equipo; no se publica ningún dato individual.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

SUMAS = {
    "pts": "points",
    "fg_att": "fg_att",
    "ft_att": "ft_att",
    "oreb": "oreb",
    "tov": "tov",
    "minutos": "minutes",
}


def extraer(parquet: Path) -> pd.DataFrame:
    df = pd.read_parquet(parquet)
    claves = ["game_id", "season", "jornada", "date", "team", "opponent", "home_away"]
    g = df.groupby(claves, as_index=False).agg(**{k: (v, "sum") for k, v in SUMAS.items()})
    # Prórrogas: 200 min de equipo en 40', +25 por cada prórroga de 5'.
    g["overtimes"] = ((g["minutos"] - 200) / 25).round().astype(int)
    rival = g[["game_id", "team", "pts", "fg_att", "ft_att", "oreb", "tov"]].rename(
        columns={
            "team": "opponent",
            "pts": "opp_pts",
            "fg_att": "opp_fg_att",
            "ft_att": "opp_ft_att",
            "oreb": "opp_oreb",
            "tov": "opp_tov",
        }
    )
    g = g.merge(rival, on=["game_id", "opponent"], validate="one_to_one")
    g["date"] = pd.to_datetime(g["date"]).dt.strftime("%Y-%m-%d")
    cols = [
        "game_id", "season", "jornada", "date", "team", "opponent", "home_away",
        "pts", "opp_pts", "overtimes",
        "fg_att", "ft_att", "oreb", "tov",
        "opp_fg_att", "opp_ft_att", "opp_oreb", "opp_tov",
    ]  # fmt: skip
    return g[cols].sort_values(["jornada", "game_id", "home_away"]).reset_index(drop=True)


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    out = extraer(Path(sys.argv[1]))
    Path(sys.argv[2]).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(sys.argv[2], index=False)
    print(f"{len(out)} filas, {out.game_id.nunique()} partidos -> {sys.argv[2]}")


if __name__ == "__main__":
    main()
