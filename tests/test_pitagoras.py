import numpy as np
import pandas as pd

from pitagorica import datos, pitagoras, simulacion
from pitagorica.estadistica import decision, desvio


def test_pitagorico_simetria_y_monotonia():
    assert pitagoras.pitagorico(100, 100, 14) == 0.5
    assert pitagoras.pitagorico(110, 100, 14) > pitagoras.pitagorico(110, 100, 5)
    assert np.isclose(pitagoras.pitagorico(90, 100, 10) + pitagoras.pitagorico(100, 90, 10), 1)


def test_ajustar_k_recupera_k_conocido():
    rng = np.random.default_rng(0)
    pf = rng.uniform(2800, 3300, 18)
    pc = rng.uniform(2800, 3300, 18)
    k_real = 11.0
    g = 10_000  # muchos partidos: sin ruido de muestreo
    v = g * pitagoras.pitagorico(pf, pc, k_real)
    assert abs(pitagoras.ajustar_k(v, np.full(18, g), pf, pc) - k_real) < 0.05


def test_posesiones_caso_a_mano():
    df = pd.DataFrame(
        {"fg_att": [60], "ft_att": [25], "oreb": [10], "tov": [12],
         "opp_fg_att": [58], "opp_ft_att": [20], "opp_oreb": [8], "opp_tov": [14]}
    )  # fmt: skip
    # off = 60 + 11 - 10 + 12 = 73 ; def = 58 + 8.8 - 8 + 14 = 72.8
    assert np.isclose(datos.posesiones(df).iloc[0], 72.9)


def test_log5_simetrico_y_calibracion_h():
    assert simulacion.prob_local(np.array([0.6]), np.array([0.6]), 1.0)[0] == 0.5
    s_l = np.array([0.5, 0.6, 0.4, 0.55])
    s_v = np.array([0.45, 0.5, 0.6, 0.5])
    h = simulacion.calibrar_h(s_l, s_v, 3)
    assert np.isclose(simulacion.prob_local(s_l, s_v, h).sum(), 3)


def test_simulacion_media_y_conservacion():
    cal = pd.DataFrame(
        {"local": ["A", "B", "C", "A", "B", "C"], "visitante": ["B", "C", "A", "C", "A", "B"],
         "pts_local": [1, 1, 0, 1, 0, 1], "pts_visit": [0, 0, 1, 0, 1, 0]}
    )  # fmt: skip
    fuerza = pd.Series({"A": 0.6, "B": 0.5, "C": 0.4})
    wins, diag = simulacion.simular(cal, fuerza, 5000, np.random.default_rng(1))
    assert (wins.sum(axis=1) == len(cal)).all()
    assert np.allclose(wins.mean(), diag["esperadas_log5"], atol=0.08)


def test_desvio_y_decision():
    t = pd.DataFrame({"V": [20], "G": [34], "PF": [3000], "PC": [3000]})
    assert np.isclose(desvio(t, 14).iloc[0], 3.0)
    a = {"ic90_bajo": 0.1}
    assert decision(a, {"p_valor": 0.05})["conclusion"] == "senal_de_habilidad"
    assert decision(a, {"p_valor": 0.2})["conclusion"] == "compatible_con_azar"
    assert decision({"ic90_bajo": -0.1}, {"p_valor": 0.01})["conclusion"] == "compatible_con_azar"


def test_csv_invariantes():
    df = datos.cargar()
    assert len(df) == 612 and df["game_id"].nunique() == 306
    assert (df.groupby("team").size() == 34).all()
    assert (df["margen"] != 0).all()
    assert df["victoria"].sum() == 306
    assert df["vuelta"].value_counts().to_dict() == {1: 306, 2: 306}
