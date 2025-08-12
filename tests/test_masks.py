from src.masks import get_mask_card_number, get_mask_account

@pytest.mark.parametrize("input_card, expected_output", [
    ("7000792289606361", "7000 79** **** 6361"),
    ("Visa 7000792289606361", "7000 79** **** 6361"),  # Проверка с лишними символами
    ("1234567890123456", "1234 56** **** 3456"),
    ("", ""),  # Пустая строка
    ("1234", "1234"),  # Слишком короткий номер
])
def test_get_mask_card_number(input_card, expected_output):
    assert get_mask_card_number(input_card) == expected_output


@pytest.mark.parametrize("input_account, expected_output", [
    ("73654108430135874305", "**4305"),
    ("1234567890", "**7890"),
    ("", ""),  # Пустая строка
    ("123", "**123"),  # Слишком короткий номер
])
def test_get_mask_account(input_account, expected_output):
    assert get_mask_account(input_account) == expected_output