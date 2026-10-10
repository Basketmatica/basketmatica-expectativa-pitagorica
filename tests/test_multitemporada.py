import numpy as np
import pandas as pd

from pitagorica import datos, pitagoras
from pitagorica import multitemporada as mt


def _ts_sintetica(k_por_temp: dict, rng) -> pd.DataFrame:
    filas = []
    for s, k in k_por_temp.items():
        pf = rng.uniform(2800, 3300, 18)
        pc = rng.uniform(2800, 3300, 18)
        g = 10_000  # sin ruido de muestreo
        v = g * pitagoras.pitagorico(pf, pc, k)
        for i in range(18):
            filas.append(
                {"season": s, "club": f"E{i}", "G": g, "V": v[i], "PF": pf[i], "PC": pc[i],
                 "pct_v": v[i] / g, "net_rtg": 0.0, "pct_ig": 0.5}
            )  # fmt: skip
    return pd.DataFrame(filas)


def test_k_sin_temporada_excluye_la_temporada():
    ts = _ts_sintetica({"a": 8.0, "b": 8.0, "c": 20.0}, np.random.default_rng(0))
    ks = mt.k_sin_temporada(ts)
    assert abs(ks["c"] - 8.0) < 0.1  # ajustado solo con a y b
    assert ks["a"] > 8.5  # mezcla de b y c


def test_pares_cadena_y_franquicias():
    df = datos.cargar_todas()
    ts = datos.tabla_temporadas(df[df["season"] != datos.TEMPORADA_EXCLUIDA])
    p = mt.pares(mt.con_desvios(ts))
    assert len(p) == 99
    assert not ((p["temporada_t"] == "2018_19") & (p["temporada_t1"] == "2020_21")).any()
    assert datos.NOMBRE_CORTO["Leyma Basquet Coruña"] == datos.NOMBRE_CORTO["Monbus Obradoiro"]


def test_persistencia_detecta_senal_y_no_en_ruido():
    rng = np.random.default_rng(1)
    n = 120
    clubes = [f"C{i % 24}" for i in range(n)]
    x = rng.normal(0, 2, n)
    base = {"club": clubes, "temporada_t": "a", "temporada_t1": "b", "desvio34_t": x}
    con_senal = pd.DataFrame({**base, "desvio34_t1": 0.6 * x + rng.normal(0, 1.5, n)})
    ruido = pd.DataFrame({**base, "desvio34_t1": rng.normal(0, 2, n)})
    a = mt.persistencia(con_senal, 1000, np.random.default_rng(2))
    b = mt.persistencia(ruido, 1000, np.random.default_rng(2))
    assert a["conclusion"] == "senal_de_habilidad" and a["r"]["ic90_bajo"] > 0
    assert b["conclusion"] == "compatible_con_azar"
    assert abs(a["pendiente"]["estimacion"] - 0.6) < 0.15
