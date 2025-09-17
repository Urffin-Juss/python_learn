import csv
import pandas as pd
import os
from dotenv import load_dotenv

# Импортируем ваш логгер
from your_logging_module import setup_logger

# Создаем логгер
logger = setup_logger(__name__)

# Загружаем настройки из .env
load_dotenv()


def read_financial_transactions_from_gsi(file_path=None):
    """Читает транзакции из CSV файла"""
    if file_path is None:
        file_path = os.getenv('GSI_FILE_PATH')

    logger.info(f"Чтение GSI файла: {file_path}")

    try:
        with open(file_path, "r", encoding="UTF-8") as file:
            reader = csv.DictReader(file)
            transactions = list(reader)
            logger.info(f"Прочитано {len(transactions)} транзакций")
            return transactions
    except Exception as e:
        logger.error(f"Ошибка чтения GSI: {e}")
        raise


def read_financial_transactions_from_excel(file_path=None):
    """Читает транзакции из Excel файла"""
    if file_path is None:
        file_path = os.getenv('EXCEL_FILE_PATH')

    logger.info(f"Чтение Excel файла: {file_path}")

    try:
        excel_data = pd.read_excel(file_path)
        transactions = excel_data.to_dict(orient="records")
        logger.info(f"Прочитано {len(transactions)} транзакций")
        return transactions
    except Exception as e:
        logger.error(f"Ошибка чтения Excel: {e}")
        raise