import coverage
import pytest
from utils import load_transactions
import json
import os
from src.masks import get_mask_card_number, get_mask_account
from src.masks import filter_by_currency, transaction_descriptions
from unittest.mock import patch, Mock
from external_api import convert_to_rub, get_exchange_rate

def test_get_mask_card_number():
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"
    assert get_mask_card_number("Visa 7000792289606361") == "7000 79** **** 6361"  # Проверка с лишними символами
    assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"

def test_get_mask_account():
    assert get_mask_account("73654108430135874305") == "**4305"
    assert get_mask_account("1234567890") == "**7890"


# Фикстура с тестовыми данными
@pytest.fixture
def sample_transactions():
    return [
        {"id": 1, "amount": 100, "currency": "USD", "description": "Purchase 1"},
        {"id": 2, "amount": 200, "currency": "EUR", "description": "Purchase 2"},
        {"id": 3, "amount": 300, "currency": "USD", "description": "Purchase 3"},
        {"id": 4, "amount": 400, "currency": "GBP", "description": ""},
        {"id": 5, "amount": 500, "description": "No currency"},
        {"id": 6, "currency": "USD", "description": "No amount"},
    ]


# Тесты для filter_by_currency
class TestFilterByCurrency:
    @pytest.mark.parametrize("currency,expected_ids", [
        ("USD", [1, 3, 6]),
        ("EUR", [2]),
        ("GBP", [4]),
        ("JPY", []),
    ])
    def test_filter_correct_currency(self, sample_transactions, currency, expected_ids):
        """Тестирование фильтрации по валюте"""
        result = list(filter_by_currency(sample_transactions, currency))
        assert [t["id"] for t in result] == expected_ids

    def test_case_insensitivity(self, sample_transactions):
        """Тестирование регистронезависимости"""
        result_lower = list(filter_by_currency(sample_transactions, "usd"))
        result_upper = list(filter_by_currency(sample_transactions, "USD"))
        assert result_lower == result_upper

    def test_empty_input(self):
        """Тестирование с пустым списком транзакций"""
        assert list(filter_by_currency([], "USD")) == []


# Тесты для transaction_descriptions
class TestTransactionDescriptions:
    @pytest.mark.parametrize("index,expected", [
        (0, "Purchase 1"),
        (1, "Purchase 2"),
        (3, ""),
        (4, "No currency"),
    ])
    def test_description_extraction(self, sample_transactions, index, expected):
        """Тестирование извлечения описаний"""
        gen = transaction_descriptions(sample_transactions)
        descriptions = list(gen)
        assert descriptions[index] == expected

    def test_all_descriptions(self, sample_transactions):
        """Тестирование полного списка описаний"""
        expected = [
            "Purchase 1", "Purchase 2", "Purchase 3",
            "", "No currency", "No amount"
        ]
        assert list(transaction_descriptions(sample_transactions)) == expected

    def test_empty_transactions(self):
        """Тестирование с пустым списком транзакций"""
        assert list(transaction_descriptions([])) == []


# Тест покрытия
def test_coverage():
    """Проверка что тесты покрывают весь функционал"""

    cov = coverage.Coverage()
    cov.start()

    # Запускаем тестируемые функции
    test_transactions = [{"currency": "USD", "description": "Test"}]
    list(filter_by_currency(test_transactions, "USD"))
    list(transaction_descriptions(test_transactions))

    cov.stop()
    cov.save()
    assert cov.report() >= 80, "Покрытие кода должно быть не менее 80%"


def test_load_nonexistent_file(tmp_path):
    """Тест загрузки несуществующего файла"""
    result = load_transactions(str(tmp_path / "nonexistent.json"))
    assert result == []

def test_load_empty_file(tmp_path):
    """Тест загрузки пустого файла"""
    empty_file = tmp_path / "empty.json"
    empty_file.touch()
    result = load_transactions(str(empty_file))
    assert result == []

def test_load_invalid_json(tmp_path):
    """Тест загрузки файла с некорректным JSON"""
    invalid_file = tmp_path / "invalid.json"
    invalid_file.write_text("{invalid json")
    result = load_transactions(str(invalid_file))
    assert result == []

def test_load_valid_transactions(tmp_path):
    """Тест загрузки корректного файла"""
    test_data = [
        {"id": 1, "amount": 100, "currency": "USD"},
        {"id": 2, "amount": 200, "currency": "EUR"}
    ]
    valid_file = tmp_path / "valid.json"
    valid_file.write_text(json.dumps(test_data))
    result = load_transactions(str(valid_file))
    assert result == test_data


@pytest.fixture
def sample_transactions():
    return [
        {"amount": "100", "currency": "RUB"},
        {"amount": "50", "currency": "USD"},
        {"amount": "75", "currency": "EUR"},
        {"amount": "200", "currency": "GBP"},
    ]


def test_convert_rub_transaction(sample_transactions):
    """Тест конвертации RUB транзакции"""
    result = convert_to_rub(sample_transactions[0])
    assert result == 100.0


@patch('external_api.requests.get')
def test_convert_usd_transaction(mock_get, sample_transactions):
    """Тест конвертации USD транзакции с моком API"""
    # Мок ответа API
    mock_response = Mock()
    mock_response.json.return_value = {"rates": {"RUB": 75.5}, "success": True}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = convert_to_rub(sample_transactions[1])
    assert result == 50 * 75.5


@patch('external_api.requests.get')
def test_api_error_handling(mock_get):
    """Тест обработки ошибок API"""
    mock_get.side_effect = requests.exceptions.ConnectionError("API unavailable")

    with pytest.raises(ConnectionError):
        get_exchange_rate("USD")


def test_missing_api_key(monkeypatch):
    """Тест отсутствия API ключа"""
    monkeypatch.delenv('EXCHANGE_RATES_API_KEY', raising=False)

    with pytest.raises(ValueError, match="API key not found"):
        get_exchange_rate("USD")


@patch('external_api.requests.get')
def test_invalid_currency(mock_get):
    """Тест невалидной валюты"""
    mock_response = Mock()
    mock_response.json.return_value = {"rates": {}, "success": True}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    with pytest.raises(ValueError, match="not found in API response"):
        get_exchange_rate("INVALID")