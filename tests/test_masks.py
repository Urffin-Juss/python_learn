import coverage

from src.masks import get_mask_card_number, get_mask_account
from src.masks import filter_by_currency, transaction_descriptions


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