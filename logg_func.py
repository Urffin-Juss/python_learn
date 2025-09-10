import sys
import functools
from datetime import datetime
from typing import Optional, Callable
import inspect


def patch_module_with_logging(module, filename: Optional[str] = None):
    """
    Патчит все функции в модуле автоматическим логированием

    Args:
        module: Модуль для патчинга
        filename: Имя файла для логирования (если None - логи в консоль)
    """
    for name in dir(module):
        obj = getattr(module, name)
        if (callable(obj) and
                not name.startswith('_') and
                not inspect.isclass(obj) and
                not inspect.ismodule(obj)):
            setattr(module, name, _add_logging_to_function(obj, filename))


def _add_logging_to_function(func: Callable, filename: Optional[str] = None):
    """Добавляет логирование к функции"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        func_name = func.__name__
        params = f"args: {args}, kwargs: {kwargs}"

        # Логируем начало выполнения
        start_entry = f"{timestamp} - {func_name} started with {params}\n"
        _write_log(start_entry, filename)

        try:
            result = func(*args, **kwargs)
            # Логируем успешное завершение
            success_entry = f"{timestamp} - {func_name} finished. Result: {result}\n"
            _write_log(success_entry, filename)
            return result

        except Exception as e:
            # Логируем ошибку
            error_entry = f"{timestamp} - {func_name} failed. Error: {type(e).__name__}: {e}\n"
            _write_log(error_entry, filename)
            raise

    return wrapper


def _write_log(message: str, filename: Optional[str] = None):
    """Записывает лог в файл или консоль"""
    if filename:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(message)
    else:
        print(message, end='')