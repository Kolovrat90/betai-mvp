import pytest
from betai.kelly import kelly_fraction

def test_kelly_fraction_positive_edge():
    # Положительный edge
    edge = 0.2  # 20% преимущество
    k_dec = 3.0  # Коэффициент 3.0
    fraction = kelly_fraction(edge, k_dec)
    assert fraction > 0
    assert round(fraction, 2) == 0.1  # Должно быть примерно 0.1 (10%)

def test_kelly_fraction_negative_edge():
    # Отрицательный edge - не должны делать ставку
    edge = -0.1  # -10% преимущество
    k_dec = 2.0  # Коэффициент 2.0
    fraction = kelly_fraction(edge, k_dec)
    assert fraction == 0.0  # Должно быть 0

def test_kelly_fraction_zero_edge():
    # Нулевой edge - не должны делать ставку
    edge = 0.0
    k_dec = 1.5
    fraction = kelly_fraction(edge, k_dec)
    assert fraction == 0.0  # Должно быть 0
