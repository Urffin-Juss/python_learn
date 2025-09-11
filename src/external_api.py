import os
import requests
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_LAYER_KEY')
BASE_URL = "https://api.apilayer.com/exchangerates_data/live?base=USD&symbols=EUR,GBP"


def convert_to_rub(transaction: Dict) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction: Словарь с данными транзакции

    Returns:
        float: Сумма в рублях
    """
    amount = float(transaction.get('amount', 0))
    currency = transaction.get('currency', 'RUB').upper()

    if currency == 'RUB':
        return amount

    # Конвертируем валюту
    rate = get_exchange_rate(currency)
    return round(amount * rate, 2)


def get_exchange_rate(currency: str) -> float:
    """
    Получает текущий курс валюты к рублю через API.

    Args:
        currency: Код валюты (USD, EUR)

    Returns:
        float: Курс валюты к рублю
    """
    if not API_KEY:
        raise ValueError("API key not found. Please set EXCHANGE_RATES_API_KEY in .env file")

    headers = {"apikey": API_KEY}
    params = {"base": currency, "symbols": "RUB"}

    try:
        response = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        return data['rates']['RUB']

    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Failed to get exchange rate: {e}")
    except KeyError:
        raise ValueError(f"Currency {currency} not found in API response")