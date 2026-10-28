"""Ejecuta el análisis pre-registrado v2 (docs/preregistro_v2.md) y escribe outputs/.

    uv run python scripts/analisis.py [--rapido]

--rapido reduce remuestreos y simulaciones (solo para depurar; no usar para publicar).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from pitagorica import K_NBA, N_BOOT, N_SIM, SEMILLA, graficos, simulacion
from pitagorica import datos as dt
from pitagorica import estadistica as est
from pitagorica import multitemporada as mt
from pitagorica import pitagoras as pg

RAIZ = Path(__file__).resolve().parents[1]
OUT = RAIZ / "outputs"
ACTUAL = dt.TEMPORADA_ACTUAL


def analisis_k_y_persistencia(ts, n_boot, rng, transiciones):
    """k fuera de muestra y test principal sobre las temporadas de `ts`."""
    val = mt.validacion_k(ts)
    td = mt.con_desvios(ts)
    p = mt.pares(td, transiciones)
    return val, td, p, mt.persistencia(p, n_boot, rng)


def bandas_por_temporada(df, td, n_sim, rng):
    """Simulación de cada temporada con su calendario; banda 90% y recuento de equipos fuera."""
    filas, rms = [], []
    for s in sorted(td["season"].unique()):
        d = df[df["season"] == s]
        cal = dt.partidos(d)
        cal["local"] = cal["local"].map(lambda e: dt.NOMBRE_CORTO.get(e, e))
        cal["visitante"] = cal["visitante"].map(lambda e: dt.NOMBRE_CORTO.get(e, e))
        x = td[td["season"] == s].set_index("club")
        wins, diag = simulacion.simular(cal, x["pyth"], n_sim, rng)
        bd = simulacion.banda(wins)
        g = x["G"]
        # bandas en victorias reales de esa temporada (G partidos)
        y = x[["V", "G", "pyth", "desvio34", "esperadas34"]].join(bd)
        y["esperadas"] = g * x["pyth"]
        y["fuera_banda"] = (y["V"] < y["p_bajo"]) | (y["V"] > y["p_alto"])
        y.insert(0, "temporada", s)
        filas.append(y.reset_index())
        r = est.contraste_varianza(y["V"] - y["esperadas"], y["esperadas"], wins)
        rms.append({"temporada": s, **r})
    return pd.concat(filas, ignore_index=True), pd.DataFrame(rms)


def main() -> None:
    rapido = "--rapido" in sys.argv
    n_sim, n_boot = (500, 500) if rapido else (N_SIM, N_BOOT)
    rng = np.random.default_rng(SEMILLA)
    (OUT / "figuras").mkdir(parents=True, exist_ok=True)
    (OUT / "tablas").mkdir(parents=True, exist_ok=True)

    df_all = dt.cargar_todas()
    usables = dt.temporadas_usables(df_all)
    df = df_all[df_all["season"].isin(usables)].reset_index(drop=True)
    ts = dt.tabla_temporadas(df)
    res: dict = {
        "temporadas_usadas": usables,
        "temporada_excluida": dt.TEMPORADA_EXCLUIDA,
        "equipos_temporada": int(len(ts)),
        "clubes": int(ts["club"].nunique()),
        "n_sim": n_sim,
        "n_boot": n_boot,
    }

    # --- k fuera de muestra ---
    val, td, p, pers = analisis_k_y_persistencia(ts, n_boot, rng, dt.TRANSICIONES)
    k_all = mt.k_conjunto(ts)
    ks_boot = mt.bootstrap_k_conjunto(df, n_boot, rng)
    ic_k = tuple(map(float, np.percentile(ks_boot, mt.NIVEL_IC)))
    mejor = int((val["error_k_sin_temporada"] < val["error_k14"]).sum())
    res["k"] = {
        "k_conjunto": k_all,
        "ic90": list(ic_k),
        "error_medio_k_sin_temporada": float(val["error_k_sin_temporada"].mean()),
        "error_medio_k14": float(val["error_k14"].mean()),
        "error_medio_k_propio": float(val["error_k_propio"].mean()),
        "temporadas_donde_gana_k_sin_temporada": mejor,
        "ic_excluye_14": bool(not (ic_k[0] <= K_NBA <= ic_k[1])),
        "difiere_de_14": bool(not (ic_k[0] <= K_NBA <= ic_k[1]) and mejor >= 5),
        "k_actual_sin_temporada": float(val.set_index("temporada").loc[ACTUAL, "k_sin_temporada"]),
    }
    val.round(3).to_csv(OUT / "tablas" / "k_por_temporada.csv", index=False)
    ks_grid = np.linspace(pg.K_MIN, pg.K_MAX, 391)
    err = np.array([mt.error_medio34(ts, k) for k in ks_grid])
    graficos.fig_curva_k_multi(
        ks_grid, err, k_all, ic_k, dict(zip(val["temporada"], val["k_propio"], strict=True))
    ).savefig(OUT / "figuras" / "fig1_curva_k.png")

    # --- test principal ---
    res["persistencia"] = pers
    res["decision"] = pers["conclusion"]
    pers_ic = (pers["r"]["ic90_bajo"], pers["r"]["ic90_alto"])
    graficos.fig_pares(p, pers["r"]["estimacion"], pers_ic, pers["n_pares"]).savefig(
        OUT / "figuras" / "fig3_pares.png"
    )
    p.round(3).to_csv(OUT / "tablas" / "pares_entre_temporadas.csv", index=False)

    # --- secundarios ---
    res["finales"] = mt.finales(p, n_boot, rng)
    res["prediccion"] = mt.prediccion(p, n_boot, rng)
    graficos.fig_prediccion_multi(res["prediccion"]).savefig(
        OUT / "figuras" / "fig4_prediccion.png"
    )

    # banda del azar por temporada
    bandas, rms = bandas_por_temporada(df, td, n_sim, rng)
    res["bandas"] = {
        "equipos_temporada": int(len(bandas)),
        "fuera_banda": int(bandas["fuera_banda"].sum()),
        "proporcion_fuera": float(bandas["fuera_banda"].mean()),
        "nominal": 0.10,
        "por_temporada": bandas.groupby("temporada")["fuera_banda"].sum().astype(int).to_dict(),
        "advertencia": "sesgo conservador: la fuerza simulada sale de los mismos puntos",
    }
    res["varianza_v1_por_temporada"] = rms.round(4).to_dict("records")

    # --- 25/26: tabla, hero, mitades ---
    b25 = bandas[bandas["temporada"] == ACTUAL].set_index("club")
    t25 = td[td["season"] == ACTUAL].set_index("club")
    tabla = pd.DataFrame(
        {
            "V": t25["V"],
            "PF": t25["PF"],
            "PC": t25["PC"],
            "pitagorico": t25["pyth"],
            "esperadas": b25["esperadas"],
            "desvio": t25["desvio34"],
        }  # fmt: skip
    ).join(b25[["p_bajo", "p_alto", "fuera_banda"]])
    bal = dt.balance_igualados(df[df["season"] == ACTUAL])
    bal.index = [dt.NOMBRE_CORTO.get(e, e) for e in bal.index]
    tabla = tabla.join(bal)
    tabla["net_rtg"] = t25["net_rtg"]
    tabla.sort_values("desvio", ascending=False).round(3).to_csv(
        OUT / "tablas" / "equipos_25_26.csv", index_label="equipo"
    )
    graficos.fig_desvios(tabla).savefig(OUT / "figuras" / "fig2_desvios.png")
    mx, mn = tabla["desvio"].idxmax(), tabla["desvio"].idxmin()
    res["temporada_actual"] = {
        "k": float(t25["k"].iloc[0]),
        "equipos_fuera_banda": tabla.index[tabla["fuera_banda"]].tolist(),
        "mayor_desvio_positivo": {
            "equipo": mx,
            "desvio": float(tabla.loc[mx, "desvio"]),
            "fuera_banda": bool(tabla.loc[mx, "fuera_banda"]),
        },  # fmt: skip
        "mayor_desvio_negativo": {
            "equipo": mn,
            "desvio": float(tabla.loc[mn, "desvio"]),
            "fuera_banda": bool(tabla.loc[mn, "fuera_banda"]),
        },  # fmt: skip
        "corr_desvio_vs_balance_igualados": float(
            np.corrcoef(tabla["desvio"], tabla["V_igualados"] - tabla["D_igualados"])[0, 1]
        ),
    }
    d25 = df[df["season"] == ACTUAL]
    t1, t2 = dt.tabla_equipos(d25, 1), dt.tabla_equipos(d25, 2)
    k25 = res["temporada_actual"]["k"]
    d1, d2 = est.desvio(t1, k25), est.desvio(t2, k25)
    res["mitades_25_26"] = est.contraste_mitades(d1, d2, n_boot, rng)

    # --- predicción 26/27 ---
    beta = max(pers["pendiente"]["estimacion"], 0.0)
    res["prediccion_26_27"] = {"beta_usada": beta}
    pred = pd.DataFrame(
        {
            "V_25_26": tabla["V"],
            "esperadas_por_puntos": tabla["esperadas"],
            "desvio_25_26": tabla["desvio"],
            "desvio_esperado_26_27": beta * tabla["desvio"],
        }  # fmt: skip
    )
    pred.sort_values("desvio_25_26", ascending=False).round(2).to_csv(
        OUT / "tablas" / "prediccion_26_27.csv", index_label="equipo"
    )

    # --- recurso: victorias esperadas de todas las temporadas ---
    rec = bandas[["temporada", "club", "V", "G", "esperadas", "desvio34", "p_bajo", "p_alto"]]
    rec = rec.assign(esperadas=rec["esperadas"].round(2), desvio34=rec["desvio34"].round(2))
    rec.rename(
        columns={"club": "equipo", "V": "victorias", "G": "partidos", "desvio34": "desvio_por_34"}
    ).to_csv(  # fmt: skip
        OUT / "tablas" / "victorias_esperadas_todas_las_temporadas.csv", index=False
    )

    # --- sensibilidad: sin 2020/21 ---
    ts_s = ts[ts["season"] != dt.TEMPORADA_DESIGUAL]
    trans_s = [t for t in dt.TRANSICIONES if dt.TEMPORADA_DESIGUAL not in t]
    val_s, _, _, pers_s = analisis_k_y_persistencia(ts_s, n_boot, rng, trans_s)
    res["sensibilidad_sin_2020_21"] = {
        "k_conjunto": mt.k_conjunto(ts_s),
        "r": pers_s["r"],
        "pendiente": pers_s["pendiente"],
        "n_pares": pers_s["n_pares"],
        "conclusion": pers_s["conclusion"],
        "temporadas_donde_gana_k_sin_temporada": int(
            (val_s["error_k_sin_temporada"] < val_s["error_k14"]).sum()
        ),
    }

    (OUT / "resultados.json").write_text(
        json.dumps(res, indent=2, ensure_ascii=False, default=float)
    )
    print(res["decision"], "| k =", round(k_all, 2), "| r =", round(pers["r"]["estimacion"], 3))


if __name__ == "__main__":
    main()
