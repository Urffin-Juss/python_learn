import json
from typing import List, Dict
import os


file_path = os.path.join('data', 'operations.json')
transactions = load_transactions(file_path)

def load_transactions(file_path: str) -> List[Dict]:
    """
    Загружает данные о финансовых транзакциях из JSON-файла.

    Args:
        file_path: Путь до JSON-файла с транзакциями

    Returns:
        List[Dict]: Список словарей с данными транзакций.
                   Возвращает пустой список если:
                   - файл не найден
                   - файл пустой
                   - файл не содержит список
                   - произошла ошибка парсинга JSON
    """
    try:
        # Проверяем существование файла
        if not os.path.exists(file_path):
            return []

        # Проверяем что файл не пустой
        if os.path.getsize(file_path) == 0:
            return []

        # Читаем и парсим JSON
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Проверяем что данные - это список
        if not isinstance(data, list):
            return []

        return data

    except (json.JSONDecodeError, IOError, OSError):
        # Обрабатываем ошибки чтения файла и парсинга JSON
        return []

def print_operations(data):
        print(f"Программа: Всего банковских операций в выборке: {len(data)}")
        for op in data:
            date = op.get("date", "")
            desc = op.get("description", "")
            amount = op.get("operationAmount", {}).get("amount", "")
            currency = op.get("operationAmount", {}).get("currency", {}).get("name", "")
            print(f"\n{date} {desc}\nСумма: {amount} {currency}")
