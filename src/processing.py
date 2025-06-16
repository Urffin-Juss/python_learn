def filter_by_state(transactions: list[dict], state: str = 'EXECUTED') -> list[dict]:
    """
    Фильтрует список словарей по значению ключа 'state'.

    Args:
        transactions: Список словарей для фильтрации
        state: Значение для фильтрации (по умолчанию 'EXECUTED')

    Returns:
        Список словарей, где state соответствует заданному значению
    """
    return [t for t in transactions if t.get('state') == state]