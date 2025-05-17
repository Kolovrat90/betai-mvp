import pytest
from betai.models import calc_edge

def test_calc_edge_positive():
    # Положительный edge: вероятность модели выше, чем у букмекера
    k_dec = 2.0  # Коэффициент 2.0 соответствует вероятности 0.5
    p_model = 0.6  # Наша модель считает вероятность 0.6
    edge = calc_edge(k_dec, p_model)
    assert edge > 0
    assert round(edge, 2) == 0.2  # Edge должен быть примерно 0.2 (20%)

def test_calc_edge_negative():
    # Отрицательный edge: вероятность модели ниже, чем у букмекера
    k_dec = 2.0  # Коэффициент 2.0 соответствует вероятности 0.5
    p_model = 0.4  # Наша модель считает вероятность 0.4
    edge = calc_edge(k_dec, p_model)
    assert edge < 0
    assert round(edge, 2) == -0.2  # Edge должен быть примерно -0.2 (-20%)

def test_calc_edge_zero():
    # Нулевой edge: вероятность модели равна вероятности букмекера
    k_dec = 2.0  # Коэффициент 2.0 соответствует вероятности 0.5
    p_model = 0.5  # Наша модель считает вероятность 0.5
    edge = calc_edge(k_dec, p_model)
    assert abs(edge) < 1e-10  # Edge должен быть примерно 0
