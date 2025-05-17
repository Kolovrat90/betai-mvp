def kelly_fraction(edge: float, k_dec: float) -> float:
    """
    Рассчитывает оптимальную долю банка для ставки по критерию Келли.
    
    Args:
        edge (float): Преимущество ставки (например, 0.1 для 10% преимущества)
        k_dec (float): Десятичный коэффициент букмекера (например, 2.5)
        
    Returns:
        float: Доля банка для ставки (от 0 до 1)
    
    Examples:
        >>> kelly_fraction(0.2, 3.0)  # Edge 20%, коэффициент 3.0
        0.1  # Рекомендуется ставить 10% банка
        
        >>> kelly_fraction(-0.1, 2.0)  # Отрицательный edge
        0.0  # Не рекомендуется делать ставку
    """
    if edge <= 0:
        return 0.0
    
    fraction = edge / (k_dec - 1)
    return fraction
