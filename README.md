# Expectativa pitagórica en la ACB

¿Ganar por encima de lo que dicen tus puntos es una habilidad que se repite o ruido de 34 partidos? Análisis de ocho temporadas de la liga regular ACB (2017/18 a 2025/26, sin la 2019/20 suspendida), con las reglas fijadas **antes** de mirar los datos.

- **Artículo:** [`articulo/articulo.md`](articulo/articulo.md)
- **Reglas:** [`docs/preregistro.md`](docs/preregistro.md) (v1) y [`docs/preregistro_v2.md`](docs/preregistro_v2.md) (v2), commiteados antes de calcular lo que describen; cronología en [`docs/apendice_metodologico.md`](docs/apendice_metodologico.md)
- **Resultados:** [`outputs/resultados.json`](outputs/resultados.json), tablas en `outputs/tablas/`, figuras en `outputs/figuras/`
- **Notebook:** [`notebooks/metodo.ipynb`](notebooks/metodo.ipynb)

## Resultado en tres líneas

- **k = 10,7** (IC90 % 10,3–11,4), menor que el 14 de la NBA; valida fuera de muestra en 6 de 8 temporadas.
- Ningún equipo de la 25/26 queda fuera de la banda del azar.
- El desvío no se repite de una temporada a la siguiente: **r = 0,05** (IC90 % −0,11 a 0,20; 99 pares). Conclusión pre-registrada: **compatible con el azar**.

## Reproducir

Requiere Python 3.12 y [uv](https://docs.astral.sh/uv/).

```bash
uv sync
make analisis   # regenera outputs/ (≈ 1 min; semilla fija)
make test
```

## Estructura

```
data/            CSV equipo-partido por temporada y diccionario
docs/            pre-registros y apéndice metodológico
src/pitagorica/  código del análisis
scripts/         analisis.py
tests/           pytest
notebooks/       metodo.ipynb
articulo/        artículo
```

## Licencia

Código MIT (`LICENSE`). Los datos proceden de acb.com y no se licencian aquí: ver `data/README.md`.
