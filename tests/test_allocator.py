import pytest
from betai.allocator import allocate_bank

def test_allocate_bank_basic():
    # Базовый тест распределения банка
    bets = [
        {"edge": 0.2, "k_dec": 3.0},
        {"edge": 0.1, "k_dec": 2.0}
    ]
    bank = 1000
    result = allocate_bank(bets, bank)
    
    # Проверяем, что все поля добавлены
    for bet in result:
        assert "kelly" in bet
        assert "fraction" in bet
        assert "risk" in bet
        assert "amount" in bet
    
    # Проверяем, что доли и суммы положительные
    for bet in result:
        assert bet["fraction"] > 0
        assert bet["amount"] > 0

def test_allocate_bank_risk_limit():
    # Тест ограничения общего риска
    bets = [
        {"edge": 0.3, "k_dec": 2.0},
        {"edge": 0.3, "k_dec": 2.0},
        {"edge": 0.3, "k_dec": 2.0}
    ]
    bank = 1000
    max_total_risk = 0.1
    
    result = allocate_bank(bets, bank, max_total_risk=max_total_risk)
    
    # Рассчитываем общий риск
    total_risk = sum(bet["risk"] for bet in result)
    
    # Проверяем, что общий риск не превышает лимит
    assert total_risk <= max_total_risk + 1e-10  # Учитываем погрешность вычислений

def test_allocate_bank_fraction_multiplier():
    # Тест множителя доли Келли
    bets = [
        {"edge": 0.2, "k_dec": 3.0}
    ]
    bank = 1000
    fraction_multiplier = 0.5
    
    result = allocate_bank(bets, bank, fraction_multiplier=fraction_multiplier)
    
    # Проверяем, что доля уменьшена в соответствии с множителем
    kelly = result[0]["kelly"]
    fraction = result[0]["fraction"]
    assert abs(fraction - kelly * fraction_multiplier) < 1e-10
