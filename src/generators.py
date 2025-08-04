from typing import Dict, Iterator

def filter_by_currency(transactions: list[Dict], currency: str) -> Iterator[Dict]:
    """
        Фильтрует транзакции по указанной валюте и возвращает итератор.

        Args:
            transactions: Список словарей с транзакциями
            currency: Код валюты для фильтрации (например, "USD")

        Returns:
            Итератор, возвращающий транзакции с заданной валютой
        """
    return (transaction for transaction in transactions
            if transaction.get('currency', '').upper() == currency.upper())