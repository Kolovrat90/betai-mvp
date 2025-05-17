from typing import List, Dict, Any
from .kelly import kelly_fraction

def allocate_bank(
    bets: List[Dict[str, Any]], 
    bank: float, 
    fraction_multiplier: float = 0.5, 
    max_total_risk: float = 0.1
) -> List[Dict[str, Any]]:
    """
    Распределяет банк между ставками, используя модифицированный критерий Келли
    с ограничением общего риска.
    
    Args:
        bets (List[Dict]): Список ставок, каждая содержит 'edge' и 'k_dec'
        bank (float): Размер банка
        fraction_multiplier (float): Множитель доли Келли (0.5 = половина от рекомендуемой доли)
        max_total_risk (float): Максимальный общий риск (доля банка)
        
    Returns:
        List[Dict]: Список ставок с добавленными полями 'fraction', 'amount', 'risk'
    """
    # Рассчитываем первоначальные доли по Келли
    for bet in bets:
        bet['kelly'] = kelly_fraction(bet['edge'], bet['k_dec'])
        bet['fraction'] = bet['kelly'] * fraction_multiplier
        bet['risk'] = bet['fraction'] / (bet['k_dec'] - 1)
    
    # Проверяем общий риск
    total_risk = sum(bet['risk'] for bet in bets)
    
    # Если общий риск превышает лимит, корректируем доли
    if total_risk > max_total_risk and total_risk > 0:
        risk_multiplier = max_total_risk / total_risk
        for bet in bets:
            bet['fraction'] = bet['fraction'] * risk_multiplier
            bet['risk'] = bet['risk'] * risk_multiplier
    
    # Рассчитываем суммы ставок
    for bet in bets:
        bet['amount'] = bet['fraction'] * bank
        
    return bets
