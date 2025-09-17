

def get_mask_card_number(card_number: str) -> str:
    """функция, которая принимает номер карты, и возвращает ее маску"""
    try:
        if not isinstance(card_number, str):
            raise TypeError("Ожидается строка, а получен другой тип данных")
        if card_number.isdigit() and len(card_number) == 16:
            formatted_number = card_number[:4] + " " + card_number[4:6] + "** **** " + card_number[-4:]
            app_logger.debug("Введенный номер карты (ЗАМАСКИРОВАННЫЙ): %s", formatted_number)
            app_logger.info("Функция выполнена успешно")
            return formatted_number
        else:
            app_logger.error("Ошибка: неправильный формат ввода")
            return None
    except TypeError as e:
        logging.error(f"Ошибка типа данных: {e}")
        return None


if __name__ == "__main__":
    result = get_mask_card_number(input("Enter your number card: "))
    print(result)


def get_mask_account(account: str) -> str:
    """функция, которая принимает номер счета, и возвращает его маску"""
    try:
        if not isinstance(account, str):
            raise TypeError("Ожидается строка, а получен другой тип данных")
        if account.isdigit() and len(account) == 20:
            mask_account = account.replace(account[0:16], "**")
            app_logger.debug("Введенный счет карты (ЗАМАСКИРОВАННЫЙ): %s", mask_account)
            app_logger.info("Функция выполнена успешно")
            return mask_account
        else:
            app_logger.error("Ошибка: неправильный формат ввода")
            return None
    except TypeError as e:
        logging.error(f"Ошибка типа данных: {e}")
        return None


if __name__ == "__main__":
    result = get_mask_account(input("Enter account: "))
    print(result)