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



def transaction_descriptions(transactions: list[Dict]) -> Iterator[str]:
    """
    Генератор, который возвращает описания транзакций по очереди.

    Args:
        transactions: Список словарей с транзакциями

    Yields:
        Описание каждой транзакции (значение по ключу 'description')
    """
    for transaction in transactions:
        yield transaction.get('description', '')