import sys
from functools import wraps
from datetime import datetime
from typing import Callable, Optional, Any


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования выполнения функций.

    Args:
        filename: Путь к файлу для записи логов. Если None - вывод в консоль.

    Returns:
        Декорированную функцию с логированием
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Формируем базовую информацию
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            func_name = func.__name__
            params = f"args: {args}, kwargs: {kwargs}"

            # Логируем начало выполнения
            start_message = f"{timestamp} - {func_name} started with {params}\n"
            _write_log(start_message, filename)

            try:
                result = func(*args, **kwargs)
                # Логируем успешное завершение
                success_message = f"{timestamp} - {func_name} finished. Result: {result}\n"
                _write_log(success_message, filename)
                return result

            except Exception as e:
                # Логируем ошибку
                error_message = (
                    f"{timestamp} - {func_name} failed. "
                    f"Error: {type(e).__name__}: {e}. "
                    f"Input: {params}\n"
                )
                _write_log(error_message, filename)
                raise  # Пробрасываем исключение дальше

        return wrapper

    return decorator


def _write_log(message: str, filename: Optional[str] = None) -> None:
    """Вспомогательная функция для записи логов"""
    if filename:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(message)
    else:
        sys.stdout.write(message)
