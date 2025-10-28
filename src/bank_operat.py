import re
from typing import List, Dict

def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """
    Ищет операции, в описании которых есть заданная строка поиска.
    Поиск нечувствителен к регистру.
    """
    pattern = re.compile(search, re.IGNORECASE)
    return [item for item in data if pattern.search(item.get('description', ''))]


def process_bank_operations(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Считает количество операций по категориям.
    Категории ищутся по подстроке в поле 'description'.
    """
    result = {category: 0 for category in categories}

    for item in data:
        description = item.get('description', '').lower()
        for category in categories:
            if category.lower() in description:
                result[category] += 1

    return result
