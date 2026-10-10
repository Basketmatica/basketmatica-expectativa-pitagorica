"""Genera notebooks/metodo.ipynb (el notebook solo llama al paquete)."""

import nbformat as nbf

nb = nbf.v4.new_notebook()
md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell
nb.cells = [
    md(
        "# Método: expectativa pitagórica en la ACB (8 temporadas)\n\nReproduce las cifras del artículo "
        "llamando al paquete `pitagorica`. Reglas en `docs/preregistro_v2.md`. Aquí se usan menos "
        "remuestreos (2000) que en `make analisis` (10.000), así que los intervalos varían algo."
    ),
    code(
        "import numpy as np, pandas as pd\n"
        "from pitagorica import datos, multitemporada as mt, K_NBA, SEMILLA\n"
        "rng = np.random.default_rng(SEMILLA)\n"
        "df_all = datos.cargar_todas()\n"
        "df = df_all[df_all['season'].isin(datos.temporadas_usables(df_all))]\n"
        "ts = datos.tabla_temporadas(df)\n"
        "print(len(ts), 'equipos-temporada de', ts['club'].nunique(), 'clubes')\n"
        "ts.head()"
    ),
    md("## Calibrar k fuera de muestra"),
    code(
        "val = mt.validacion_k(ts)\n"
        "print('k conjunto =', round(mt.k_conjunto(ts), 2))\n"
        "print('error medio k_sin_temporada:', round(val['error_k_sin_temporada'].mean(), 2),\n"
        "      '| con k=14:', round(val['error_k14'].mean(), 2))\n"
        "val.round(2)"
    ),
    md("## Desvíos y pares t → t+1"),
    code(
        "td = mt.con_desvios(ts)\n"
        "p = mt.pares(td)\n"
        "print(len(p), 'pares')\n"
        "td[td['season'] == '2025_26'].sort_values('desvio34', ascending=False)"
        "[['club', 'V', 'esperadas34', 'desvio34']].round(2)"
    ),
    md("## ¿Se repite? Test principal pre-registrado"),
    code(
        "res = mt.persistencia(p, 2000, rng)\n"
        "print({k: res[k] for k in ('r', 'pendiente', 'n_pares', 'conclusion')})"
    ),
]
nbf.write(nb, "notebooks/metodo.ipynb")
