# Datos

`acb_partidos_<temporada>.csv` — Liga regular ACB, una temporada por fichero: 2017/18 a 2025/26. Un registro por equipo y partido (612 filas = 306 partidos × 2 en una temporada de 18 equipos). Solo totales de equipo; no contiene datos individuales.

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

Recopilados por Basketmática mediante scraping de acb.com (boxscores de liga regular) y agregados a totales de equipo y partido. La ACB es la fuente de los datos originales.

## Particularidades por temporada

| Temporada | Partidos | Equipos | Partidos por equipo | Nota |
|---|---:|---:|---|---|
| 2017/18, 2018/19, 2021/22 a 2025/26 | 306 | 18 | 34 | Normales |
| 2019/20 | 229 | 18 | 22 a 27 | **Suspendida por la pandemia, incompleta y desigual**: no se usa en el análisis |
| 2020/21 | 342 | 19 | 36 | Liga de 19 equipos; se usa con tasas (por partido) |

## Franquicias

El nombre del equipo cambia con el patrocinador. Para emparejar temporadas se usa esta equivalencia (`src/pitagorica/datos.py`): Montakit / Urbas / Baloncesto / Carplus Fuenlabrada → Fuenlabrada; Barça Lassa → FC Barcelona; Delteco / Acunsa GBC → GBC; Monbus Obradoiro / Leyma Basquet Coruña → Obradoiro.

## Comprobaciones

Cada partido tiene exactamente dos filas coherentes (marcadores y rivales cruzados), sin valores nulos y sin empates. Prórrogas: columna `overtimes`.

## Licencia y uso

Los marcadores y estadísticas de partido proceden de acb.com. **No se concede licencia sobre los datos de origen**: se publican solo totales de equipo y partido, con fines de análisis y reproducibilidad, y sin garantía alguna. Si vas a reutilizarlos, comprueba los términos de uso de acb.com. El código del repositorio es MIT (ver `LICENSE`).
