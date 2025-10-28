import sys
from src.trans_from_file import (
    read_financial_transactions_from_csv,
    read_financial_transactions_from_excel,
    read_financial_transactions_from_json)
from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date, filter_by_keyword
from src.utils import print_operations


def main():
    print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    file_choice = input("Пользователь: ")

    file_map = {
        "1": ("JSON", load_transactions),
        "2": ("CSV", read_financial_transactions_from_csv),
        "3": ("XLSX", read_financial_transactions_from_excel),
    }

    if file_choice not in file_map:
        print("Программа: Некорректный выбор файла. Завершение работы.")
        sys.exit()

    file_type, loader = file_map[file_choice]
    print(f"Программа: Для обработки выбран {file_type}-файл.")

    # Загружаем данные
    data = loader()
    if not data:
        print("Программа: Не удалось загрузить данные.")
        sys.exit()

    # --- Фильтрация по статусу ---
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        print(f"Программа: Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные статусы: EXECUTED, CANCELED, PENDING")
        status = input("Пользователь: ").strip().upper()

        if status not in valid_statuses:
            print(f'Программа: Статус операции "{status}" недоступен.')
            continue
        break

    filtered = filter_by_state(data, status)
    if not filtered:
        print("Программа: Не найдено ни одной транзакции, подходящей под условия фильтрации.")
        sys.exit()
    print(f'Программа: Операции отфильтрованы по статусу "{status}"')

    # --- Сортировка ---
    sort_choice = input("Программа: Отсортировать операции по дате? Да/Нет\nПользователь: ").strip().lower()
    if sort_choice == "да":
        direction = input("Программа: По возрастанию или по убыванию?\nПользователь: ").strip().lower()
        reverse = direction == "по убыванию"
        filtered = sort_by_date(filtered, reverse=reverse)

    # --- Фильтрация по валюте ---
    currency_choice = input("Программа: Выводить только рублевые транзакции? Да/Нет\nПользователь: ").strip().lower()
    if currency_choice == "да":
        filtered = filter_by_currency(filtered, "RUB")

    # --- Фильтрация по слову ---
    keyword_choice = input("Программа: Отфильтровать по слову в описании? Да/Нет\nПользователь: ").strip().lower()
    if keyword_choice == "да":
        word = input("Пользователь: Введите слово для поиска: ").strip()
        filtered = filter_by_keyword(filtered, word)

    # --- Итог ---
    if not filtered:
        print("Программа: Не найдено ни одной транзакции, подходящей под условия фильтрации.")
    else:
        print("Программа: Распечатываю итоговый список транзакций...")
        print_operations(filtered)


if __name__ == "__main__":
    main()
