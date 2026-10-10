"""Genera notebooks/metodo.ipynb (el notebook solo llama al paquete)."""

import nbformat as nbf

nb = nbf.v4.new_notebook()
md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell
nb.cells = [
    md(
        "# Método: expectativa pitagórica en la ACB 25/26\n\nReproduce las cifras del artículo "
        "llamando al paquete `pitagorica`. Reglas en `docs/preregistro.md`."
    ),
    code(
        "import numpy as np, pandas as pd\n"
        "from pitagorica import datos, pitagoras, simulacion, estadistica as est, K_NBA, SEMILLA\n"
        "rng = np.random.default_rng(SEMILLA)\n"
        "df = datos.cargar()\n"
        "t, t1, t2 = datos.tabla_equipos(df), datos.tabla_equipos(df, 1), datos.tabla_equipos(df, 2)\n"
        "t.head()"
    ),
    md("## Calibrar k"),
    code(
        "k = pitagoras.ajustar_k_tabla(t)\n"
        "print('k ACB =', round(k, 2), '| error medio:', round(pitagoras.error_medio(t, k), 2),\n"
        "      '| con k=14:', round(pitagoras.error_medio(t, K_NBA), 2))\n"
        "print(pitagoras.validacion_mitades(t1, t2))\n"
        "print(pitagoras.validacion_loo(t))"
    ),
    md("## Desvíos y banda del azar (simulación log5)"),
    code(
        "pyth = pd.Series(pitagoras.pitagorico(t['PF'], t['PC'], k), index=t.index)\n"
        "wins_sim, diag = simulacion.simular(datos.partidos(df), pyth, 2000, rng)\n"
        "tabla = pd.DataFrame({'V': t['V'], 'esperadas': t['G'] * pyth}).join(simulacion.banda(wins_sim))\n"
        "tabla['desvio'] = tabla['V'] - tabla['esperadas']\n"
        "tabla.sort_values('desvio', ascending=False).round(2)"
    ),
    md("## ¿Se repite? (2000 simulaciones aquí; el artículo usa 10.000: `make analisis`)"),
    code(
        "d1, d2 = est.desvio(t1, k), est.desvio(t2, k)\n"
        "a = est.contraste_mitades(d1, d2, 2000, rng)\n"
        "b = est.contraste_varianza(tabla['desvio'], tabla['esperadas'], wins_sim)\n"
        "print(a); print(b); print(est.decision(a, b))"
    ),
]
nbf.write(nb, "notebooks/metodo.ipynb")
