import csv
import pandas as pd
import os
from dotenv import load_dotenv
from logg_func import setup_logging

# Загружаем настройки из .env
load_dotenv()
logger = setup_logging(filename='financial_reader.log', level=logging.INFO)

def read_financial_transactions_from_csv(file_path= None):
    """Читает транзакции из CSV файла"""
    if file_path is None:
        file_path = os.getenv('CSV_FILE_PATH')
    logger.info(f"Чтение  CSV файла: {file_path}")

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