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


def sort_by_date(transactions: list[dict], reverse: bool = True) -> list[dict]:
    """
    Сортирует список словарей по дате (ключ 'date').

    Args:
        transactions: Список словарей с транзакциями
        reverse: Если True (по умолчанию) - сортировка по убыванию (новые сначала),
                 если False - по возрастанию (старые сначала)

    Returns:
        Отсортированный список словарей
    """

def get_date(item):
    date_str = item.get('date')
    if date_str:
        try:
            return datetime.fromisoformat(date_str)
        except (ValueError, TypeError):
            return datetime.min  # Для некорректных дат
    return datetime.min  # Для отсутствующих дат

return sorted(transactions, key=get_date, reverse=reverse)