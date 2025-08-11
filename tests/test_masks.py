import coverage
import os
from src.masks import get_mask_card_number, get_mask_account
from src.masks import filter_by_currency, transaction_descriptions
import decorators.py
from typing import Callable




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


# Фикстура для тестовой функции
@pytest.fixture
def test_function() -> Callable:
    @log()
    def sample_func(x: int, y: int = 0) -> int:
        """Тестовая функция для логирования"""
        if y < 0:
            raise ValueError("y must be non-negative")
        return x + y

    return sample_func


# Фикстура для тестового файла
@pytest.fixture
def log_file(tmp_path) -> str:
    return os.path.join(tmp_path, "test.log")


# Тесты для логирования в консоль
class TestConsoleLogging:
    def test_successful_execution(self, test_function, capsys):
        """Тест логирования успешного выполнения"""
        result = test_function(2, 3)

        captured = capsys.readouterr()
        logs = captured.out.splitlines()

        assert result == 5
        assert "sample_func started" in logs[0]
        assert "sample_func finished. Result: 5" in logs[1]
        assert len(logs) == 2

    def test_error_handling(self, test_function, capsys):
        """Тест логирования ошибки"""
        with pytest.raises(ValueError):
            test_function(2, -1)

        captured = capsys.readouterr()
        logs = captured.out.splitlines()

        assert "sample_func started" in logs[0]
        assert "sample_func failed" in logs[1]
        assert "ValueError: y must be non-negative" in logs[1]
        assert len(logs) == 2


# Тесты для логирования в файл
class TestFileLogging:
    def test_file_logging_success(self, log_file):
        """Тест записи логов успешного выполнения в файл"""

        @log(log_file)
        def file_func(a: int, b: int) -> int:
            return a * b

        result = file_func(3, 4)

        with open(log_file, 'r') as f:
            logs = f.read().splitlines()

        assert result == 12
        assert "file_func started" in logs[0]
        assert "file_func finished. Result: 12" in logs[1]
        assert len(logs) == 2

    def test_file_logging_error(self, log_file):
        """Тест записи логов ошибки в файл"""

        @log(log_file)
        def error_func():
            raise RuntimeError("Test error")

        with pytest.raises(RuntimeError):
            error_func()

        with open(log_file, 'r') as f:
            logs = f.read().splitlines()

        assert "error_func started" in logs[0]
        assert "error_func failed" in logs[1]
        assert "RuntimeError: Test error" in logs[1]
        assert len(logs) == 2


# Тест метаданных функции
def test_function_metadata_preserved(test_function):
    """Тест сохранения метаданных функции"""
    assert test_function.__name__ == "sample_func"
    assert test_function.__doc__ == "Тестовая функция для логирования"


# Тест временных меток
def test_timestamp_format(test_function, capsys):
    """Тест формата временных меток в логах"""
    test_function(1, 1)
    captured = capsys.readouterr()

    timestamp = captured.out.split(' - ')[0]
    try:
        datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        pytest.fail("Invalid timestamp format")