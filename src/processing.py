from datetime import datetime
from typing import Dict, Any


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


def get_date(item: Dict[str, Any]) -> datetime:
    """
    Извлекает дату из элемента транзакции.

    Args:
        item: Словарь с данными транзакции

    Returns:
        datetime: Объект datetime или datetime.min для некорректных/отсутствующих дат
    """
    date_str = item.get('date')

    if date_str:
        try:
            # Пробуем разные форматы дат
            if isinstance(date_str, str):
                return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            elif hasattr(date_str, 'strftime'):  # Если это уже datetime объект
                return date_str
        except (ValueError, TypeError):
            pass

    return datetime.min  # Для некорректных или отсутствующих дат
