# Apéndice metodológico

Detalle que el artículo resume. Todo lo de aquí se puede comprobar en el historial de git.

## Cronología de las reglas

| Paso | Commit | Qué se había visto |
|---|---|---|
| Pre-registro v1: solo la 25/26 | `c0c12be` | Victorias, PF y PC por equipo de la 25/26. Ningún pitagórico, k ni desvío. |
| Datos de 2017/18 a 2024/25 | `9d388a5` | Nada: solo se añadieron ficheros. |
| Pre-registro v2: ocho temporadas | `8d42f05` | Resultados completos del análisis v1 sobre la 25/26. De las temporadas nuevas, solo comprobaciones estructurales (filas, nulos, empates, nombres de equipo, número de pares). |
| Análisis v2 | `87963a7` | Resultados del test principal v2. |

Los documentos: [`preregistro.md`](preregistro.md) (v1) y [`preregistro_v2.md`](preregistro_v2.md) (v2).

## El cambio de regla entre v1 y v2

El v1 tenía dos tests. El **test B** comparaba la dispersión de los desvíos con la de temporadas simuladas por azar. En la 25/26 salió muy por debajo del azar (p = 0,96). El v2 lo sacó de la regla de decisión. **Ese cambio está motivado por haber visto el resultado de v1**, y así consta en el propio v2.

El motivo técnico: en la simulación, la fuerza de cada equipo sale de los mismos puntos de la temporada, que ya contienen parte de la suerte. Eso comprime los desvíos observados frente a los simulados, sea cual sea la realidad. Repetido en las ocho temporadas, el patrón es constante:

| Temporada | Dispersión observada (RMS, victorias) | Mediana simulada por azar |
|---|---:|---:|
| 2017/18 | 2,01 | 2,51 |
| 2018/19 | 1,67 | 2,55 |
| 2020/21 | 1,97 | 2,60 |
| 2021/22 | 1,83 | 2,61 |
| 2022/23 | 1,72 | 2,55 |
| 2023/24 | 1,91 | 2,58 |
| 2024/25 | 2,10 | 2,56 |
| 2025/26 | 1,83 | 2,56 |

Una dispersión sistemáticamente un 25-30 % menor en todas las temporadas apunta a un artefacto del método y no a una propiedad de la ACB. Por eso el test se mantiene solo como dato descriptivo, y por eso la banda del azar es conservadora: solo 2 de 145 equipos-temporada quedaron fuera de ella, frente al 10 % nominal.

El test que sustituye a B (correlación entre el desvío de una temporada y el de la siguiente) no sufre ese problema, porque no necesita una distribución nula simulada.

## Test principal y su equivalencia con un test clásico

«El límite inferior del IC al 90 % de r supera 0» equivale a un test unilateral al 5 %, solo que con intervalo bootstrap por clubes en lugar de fórmula. No se ha calculado ningún otro test para no ajustar la regla al resultado ya conocido (r = 0,05).

## Potencia

Con 99 pares, ignorando la dependencia entre pares y con un test unilateral al 10 %, la potencia aproximada es del 76 % para r = 0,20, del 89 % para r = 0,25 y del 96 % para r = 0,30. Un efecto de r ≈ 0,10 no es detectable con estos datos. El intervalo observado (−0,11 a +0,20) es coherente con esto.

## Otras comprobaciones

- **Sin la 2020/21** (19 equipos, 36 partidos): r = 0,02 (IC90 %: −0,18 a 0,20) con 82 pares. Misma conclusión.
- **Correlación por transición:** las seis van de −0,27 a +0,27, con 16-17 pares cada una.
- **Mitades de la 25/26** (J1-17 frente a J18-34): r = −0,01 (IC90 %: −0,31 a 0,32).
- **Partidos igualados:** el % de victorias en igualados de un año frente al siguiente da r = 0,13 (−0,07 a 0,30).
- **k:** el k de cada temporada por separado va de 9,2 a 12,2. El IC90 % del k conjunto (10,3 a 11,4) viene de un bootstrap de partidos y no recoge esa heterogeneidad entre temporadas.
