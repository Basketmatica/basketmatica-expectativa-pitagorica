# Expectativa pitagórica en la ACB

¿Ganar por encima de lo que dicen tus puntos es una habilidad que se repite o ruido de 34 partidos? Análisis de ocho temporadas de la liga regular ACB (2017/18 a 2025/26, sin la 2019/20 suspendida), con las reglas fijadas **antes** de mirar los datos.

- **Artículo:** [`articulo/articulo.md`](articulo/articulo.md)
- **Pre-registros:** [`docs/preregistro.md`](docs/preregistro.md) (v1, solo 25/26) y [`docs/preregistro_v2.md`](docs/preregistro_v2.md) (v2, ocho temporadas), ambos commiteados antes de calcular lo que describen
- **Resultados:** [`outputs/resultados.json`](outputs/resultados.json), tablas en `outputs/tablas/`, figuras en `outputs/figuras/`. El análisis v1 se conserva en `outputs/v1/`
- **Notebook (method drop):** [`notebooks/metodo.ipynb`](notebooks/metodo.ipynb)

## Resultado en tres líneas

- **k = 10,7** (IC90 % 10,3–11,4), menor que el 14 de la NBA; valida fuera de muestra en 6 de 8 temporadas.
- Ningún equipo de la 25/26 queda fuera de la banda del azar.
- El desvío no se repite de una temporada a la siguiente: **r = 0,05** (IC90 % −0,11 a 0,20; 99 pares). Conclusión pre-registrada: **compatible con el azar**. Un efecto de r ≈ 0,25 o más habría sido detectado con alta probabilidad; uno pequeño no se puede descartar.

## Reproducir

Requiere Python 3.12 y [uv](https://docs.astral.sh/uv/). No depende de ningún otro repositorio.

```bash
uv sync
make analisis   # regenera outputs/ (≈ 1 min; semilla fija)
make test
```

`scripts/analisis_v1.py` reproduce el análisis v1 (solo 25/26) en `outputs/v1/`. `scripts/extraer_partidos.py` es opcional: regenera un CSV desde un parquet de boxscores propio.

## Estructura

```
data/            CSV equipo-partido por temporada (9 ficheros) y diccionario
docs/            pre-registros v1 y v2
src/pitagorica/  datos, pitagoras (k), simulacion (log5), estadistica (v1),
                 multitemporada (k fuera de muestra y test entre temporadas), graficos
scripts/         analisis.py (v2), analisis_v1.py, extraer_partidos.py, hacer_notebook.py
tests/           pytest
notebooks/       metodo.ipynb
articulo/        artículo web en Markdown
```

## Licencia

Código MIT (`LICENSE`). Datos CC BY 4.0 (atribución: Basketmática), ver `data/README.md`.
