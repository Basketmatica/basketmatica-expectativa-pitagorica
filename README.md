# Expectativa pitagórica en la ACB

¿Ganar por encima de lo que dicen tus puntos es una habilidad que se repite o ruido de 34 partidos? Análisis de la liga regular ACB 2025/26, con las reglas fijadas **antes** de mirar los datos.

- **Artículo:** [`articulo/articulo.md`](articulo/articulo.md)
- **Pre-registro** (commit anterior a cualquier cálculo): [`docs/preregistro.md`](docs/preregistro.md)
- **Resultados:** [`outputs/resultados.json`](outputs/resultados.json), tablas en `outputs/tablas/`, figuras en `outputs/figuras/`
- **Notebook (method drop):** [`notebooks/metodo.ipynb`](notebooks/metodo.ipynb)

## Resultado en una línea

k ≈ 11,3 (IC90 % 9,8–13,3) y ningún equipo fuera de la banda del azar; los desvíos no se repiten entre vueltas (r = −0,02). Conclusión pre-registrada: **compatible con el azar** (una temporada y 18 equipos: poca potencia, no es una prueba de que sea suerte).

## Reproducir

Requiere Python 3.12 y [uv](https://docs.astral.sh/uv/). No depende de ningún otro repositorio.

```bash
uv sync
make analisis   # regenera outputs/ (≈ 1 min; semilla fija)
make test
```

`scripts/extraer_partidos.py` es opcional: regenera el CSV desde un parquet de boxscores propio. El CSV ya está en `data/`.

## Estructura

```
data/            CSV equipo-partido (612 filas) y diccionario
docs/            pre-registro
src/pitagorica/  datos, pitagoras (k y validación), simulacion (log5), estadistica (tests), graficos
scripts/         analisis.py, extraer_partidos.py
tests/           pytest
notebooks/       metodo.ipynb
articulo/        artículo web en Markdown
```

## Licencia

Código MIT (`LICENSE`). Datos CC BY 4.0 (atribución: Basketmática), ver `data/README.md`.
