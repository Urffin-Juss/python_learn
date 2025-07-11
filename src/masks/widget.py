def mask_account_card(account_info: str) -> str:
    """
    Маскирует номер карты или счета в переданной строке.

    Args:
        account_info: Строка с информацией о карте/счете (например "Visa Platinum 7000792289606361")

    Returns:
        str: Строка с замаскированным номером (например "Visa Platinum 7000 79** **** 6361")
    """
    # Разделяем строку на части
    parts = account_info.split()

    # Определяем тип (карта или счет)
    if parts[0].lower() == 'счет':
        # Маскировка счета
        account_number = parts[-1]
        masked_number = f"**{account_number[-4:]}" if len(account_number) > 4 else "**"
        return f"Счет {masked_number}"
    else:
        # Маскировка карты
        card_number = parts[-1]
        if len(card_number) != 16 or not card_number.isdigit():
            return account_info

        # Форматирование номера карты
        masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
        return ' '.join(parts[:-1] + [masked])


from datetime import datetime


def get_date(iso_date_string: str) -> str:
    """
    Преобразует дату из формата ISO 8601 в формат 'ДД.ММ.ГГГГ'

    Args:
        iso_date_string: Строка с датой в формате "2024-03-11T02:26:18.671407"

    Returns:
        str: Дата в формате "11.03.2024"
    """
    try:

        dt = datetime.fromisoformat(iso_date_string)

        return dt.strftime("%d.%m.%Y")
    except (ValueError, TypeError):

        return ""