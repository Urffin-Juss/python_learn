import sys
import functools
from datetime import datetime
from typing import Optional, Callable
import inspect
import logging


def setup_logging(filename: Optional[str] = None, level=logging.Debug):
    """
        Настраивает логирование для модуля

        Args:
            filename: Имя файла для логирования
            level: Уровень логирования
        """
    logger = logging.getLogger(__name__)
    logger.setLevel(level)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Обработчик (файл или консоль)
    if filename:
        handler = logging.FileHandler(filename, encoding='utf-8')
    else:
        handler = logging.StreamHandler(sys.stdout)

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def patch_module_with_logging(module, filename: Optional[str] = None):

    logger = setup_logging(filename, logging.DEBUG)

    for name in dir(module):
        obj = getattr(module, name)
        if (_is_loggable_function(obj, name)):
            setattr(module, name, _add_logging_to_function(obj, logger))


def _is_loggable_function(obj, name: str) -> bool:
    """Проверяет, нужно ли добавлять логирование к функции"""
    return (callable(obj) and
            not name.startswith('_') and
            not inspect.isclass(obj) and
            not inspect.ismodule(obj))


def _add_logging_to_function(func: Callable, logger: logging.Logger):
    """Добавляет логирование к функции"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__

        # Логируем начало выполнения
        logger.debug(f"{func_name} started with args: {args}, kwargs: {kwargs}")

        try:
            result = func(*args, **kwargs)
            # Логируем успешное завершение
            logger.debug(f"{func_name} finished. Result: {result}")
            return result

        except Exception as e:
            # Логируем ошибку
            logger.error(f"{func_name} failed. Error: {type(e).__name__}: {e}")
            raise

    return wrapper