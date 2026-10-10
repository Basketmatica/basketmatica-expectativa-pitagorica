"""Ejecuta todo el análisis pre-registrado y escribe outputs/.

    uv run python scripts/analisis.py [--rapido]

--rapido reduce remuestreos y simulaciones (solo para depurar; no usar para publicar).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from pitagorica import K_NBA, N_BOOT, N_SIM, SEMILLA, datos, graficos, pitagoras, simulacion
from pitagorica import estadistica as est

RAIZ = Path(__file__).resolve().parents[1]
OUT = RAIZ / "outputs"


def main() -> None:
    rapido = "--rapido" in sys.argv
    n_sim, n_boot = (500, 500) if rapido else (N_SIM, N_BOOT)
    rng = np.random.default_rng(SEMILLA)
    (OUT / "figuras").mkdir(parents=True, exist_ok=True)
    (OUT / "tablas").mkdir(parents=True, exist_ok=True)

    df = datos.cargar()
    t, t1, t2 = datos.tabla_equipos(df), datos.tabla_equipos(df, 1), datos.tabla_equipos(df, 2)
    cal = datos.partidos(df)
    res: dict = {
        "partidos": int(df["game_id"].nunique()),
        "equipos": int(len(t)),
        "partidos_igualados": int(df[df["igualado"]]["game_id"].nunique()),
        "partidos_con_prorroga": int(df[df["overtimes"] > 0]["game_id"].nunique()),
        "n_sim": n_sim,
        "n_boot": n_boot,
    }

    # --- 4. Calibrar k ---
    k = pitagoras.ajustar_k_tabla(t)
    ks = np.linspace(pitagoras.K_MIN, pitagoras.K_MAX, 391)
    err = pitagoras.curva_error(t, ks)
    ks_boot = pitagoras.bootstrap_k(df, n_boot, rng)
    ic_k = tuple(np.percentile(ks_boot, est.NIVEL_IC))
    res["k"] = {
        "k_acb": k,
        "ic90": list(map(float, ic_k)),
        "error_medio_acb": pitagoras.error_medio(t, k),
        "error_medio_k14": pitagoras.error_medio(t, K_NBA),
        "validacion_mitades": pitagoras.validacion_mitades(t1, t2),
        "validacion_loo": pitagoras.validacion_loo(t),
    }
    graficos.fig_curva_k(ks, err, k, ic_k).savefig(OUT / "figuras" / "fig1_curva_k.png")

    # --- 5. Temporada por equipo + simulación ---
    pyth = pd.Series(pitagoras.pitagorico(t["PF"], t["PC"], k), index=t.index)
    wins_sim, diag = simulacion.simular(cal, pyth, n_sim, rng)
    bd = simulacion.banda(wins_sim)
    tabla = pd.DataFrame(
        {
            "V": t["V"],
            "PF": t["PF"],
            "PC": t["PC"],
            "pitagorico": pyth,
            "esperadas": t["G"] * pyth,
        }  # fmt: skip
    )
    tabla["desvio"] = tabla["V"] - tabla["esperadas"]
    tabla = tabla.join(bd)
    tabla["fuera_banda"] = (tabla["V"] < tabla["p_bajo"]) | (tabla["V"] > tabla["p_alto"])
    tabla = tabla.join(datos.balance_igualados(df))
    tabla["net_rtg"] = t["net_rtg"]
    tabla.sort_values("desvio", ascending=False).round(3).to_csv(
        OUT / "tablas" / "equipos_25_26.csv", index_label="equipo"
    )
    graficos.fig_desvios(tabla).savefig(OUT / "figuras" / "fig2_desvios.png")
    res["simulacion"] = {
        "h": diag["h"],
        "pct_local_observado": diag["pct_local_observado"],
        "dif_max_esperadas_log5_vs_pitagorico": float(
            (diag["esperadas_log5"] - tabla["esperadas"]).abs().max()
        ),
        "equipos_fuera_banda": tabla.index[tabla["fuera_banda"]].tolist(),
        "mayor_desvio_positivo": {
            "equipo": tabla["desvio"].idxmax(),
            "desvio": float(tabla["desvio"].max()),
            "fuera_banda": bool(tabla.loc[tabla["desvio"].idxmax(), "fuera_banda"]),
        },  # fmt: skip
        "mayor_desvio_negativo": {
            "equipo": tabla["desvio"].idxmin(),
            "desvio": float(tabla["desvio"].min()),
            "fuera_banda": bool(tabla.loc[tabla["desvio"].idxmin(), "fuera_banda"]),
        },  # fmt: skip
    }
    ig = df[df["igualado"]]
    res["igualados"] = {
        "partidos": res["partidos_igualados"],
        "corr_desvio_vs_balance_igualados": float(
            np.corrcoef(tabla["desvio"], tabla["V_igualados"] - tabla["D_igualados"])[0, 1]
        ),
        "victorias_local_en_igualados": float(ig[ig["home_away"] == "home"]["victoria"].mean()),
    }

    # --- 6. ¿Se repite? ---
    d1, d2 = est.desvio(t1, k), est.desvio(t2, k)
    a = est.contraste_mitades(d1, d2, n_boot, rng)
    b = est.contraste_varianza(tabla["desvio"], tabla["esperadas"], wins_sim)
    res["test_a_mitades"], res["test_b_varianza"] = a, b
    res["decision"] = est.decision(a, b)
    graficos.fig_mitades(d1, d2, a["r"], (a["ic90_bajo"], a["ic90_alto"])).savefig(
        OUT / "figuras" / "fig3_mitades.png"
    )
    pd.DataFrame({"desvio_v1": d1, "desvio_v2": d2}).round(3).to_csv(
        OUT / "tablas" / "desvios_por_vuelta.csv", index_label="equipo"
    )

    # --- 7. NetRtg ---
    res["comparacion_predictiva"] = est.comparacion_predictiva(t1, t2, n_boot, rng)
    graficos.fig_prediccion(res["comparacion_predictiva"]).savefig(
        OUT / "figuras" / "fig4_prediccion.png"
    )

    # --- 8. Referencia 26/27: victorias esperadas por pitagórico, solo con 25/26 ---
    (OUT / "tablas" / "victorias_esperadas_25_26.csv").write_text(
        tabla[["V", "esperadas", "desvio"]].round(2).to_csv(index_label="equipo")
    )

    (OUT / "resultados.json").write_text(
        json.dumps(res, indent=2, ensure_ascii=False, default=float)
    )
    print(json.dumps(res["decision"]), "k =", round(k, 2))


if __name__ == "__main__":
    main()
