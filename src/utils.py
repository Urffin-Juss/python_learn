import json
from typing import List, Dict
import os
from logg_func import patch_module_with_logging
import sys


file_path = os.path.join('data', 'operations.json')


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


patch_module_with_logging(sys.modules[__name__], 'log_utils.log')
