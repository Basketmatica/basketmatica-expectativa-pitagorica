# Datos

`acb_partidos_2025_26.csv` — Liga regular ACB 2025/26. Un registro por equipo y partido (612 filas = 306 partidos × 2). Solo totales de equipo; no contiene datos individuales.

| Columna | Descripción |
|---|---|
| `game_id` | Identificador del partido en la ACB |
| `season` | Temporada (`2025_26`) |
| `jornada` | Jornada (1-34) |
| `date` | Fecha (YYYY-MM-DD) |
| `team`, `opponent` | Equipo y rival |
| `home_away` | `home` / `away` desde el punto de vista de `team` |
| `pts`, `opp_pts` | Puntos a favor y en contra (incluyen prórroga) |
| `overtimes` | Prórrogas jugadas (deducidas de los minutos de equipo: 200 + 25 por prórroga) |
| `fg_att`, `ft_att`, `oreb`, `tov` | Tiros de campo intentados, tiros libres intentados, rebotes ofensivos y pérdidas del equipo |
| `opp_*` | Lo mismo para el rival |

## Procedencia

Derivado de los boxscores públicos de acb.com, agregados a totales de equipo con `scripts/extraer_partidos.py`. Los marcadores y estadísticas de partido son datos públicos; la procedencia exacta del parquet de origen es un repositorio privado de Basketmática que no es necesario para reproducir nada de este proyecto.

## Comprobaciones

612 filas, 306 partidos, 34 partidos por equipo, sin empates, 11 partidos con prórroga (10 con una, 1 con dos).

## Licencia

Datos bajo [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (atribución: Basketmática). El código del repositorio es MIT (ver `LICENSE`).
