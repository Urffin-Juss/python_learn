


def test_mask_account_card(input_data, expected):
    assert mask_account_card(input_data) == expected


def test_get_date(input_date, expected):
    assert get_date(input_date) == expected



def test_dates():
    return [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2025-12-31T23:59:59.999999", "31.12.2025"),
    ]

# Тест с использованием фикстуры
def test_get_date_with_fixture(test_dates):
    for input_date, expected in test_dates:
        assert get_date(input_date) == expected