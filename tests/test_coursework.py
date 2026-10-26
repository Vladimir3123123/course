import pytest
from unittest.mock import patch
import pandas as pd

from src.views import get_greeting, get_cards_info, get_top_transactions
from src.services import simple_search
from src.utils import get_currency_rates, get_stock_prices


# --- ТЕСТЫ ДЛЯ VIEWS ---

@pytest.mark.parametrize("hour,expected", [
    (8, "Доброе утро"),
    (14, "Добрый день"),
    (20, "Добрый вечер"),
    (2, "Доброй ночи")
])
def test_get_greeting(hour, expected):
    from datetime import datetime
    dt = datetime(2023, 1, 1, hour, 0)
    assert get_greeting(dt) == expected


@pytest.fixture
def sample_df():
    return pd.DataFrame([
        {"card_from": "Visa 1234", "amount": 1000, "date": pd.Timestamp("2023-11-01"), "description": "Test"},
        {"card_from": "Visa 1234", "amount": 2000, "date": pd.Timestamp("2023-11-02"), "description": "Test 2"},
        {"card_from": "Mastercard 5678", "amount": 500, "date": pd.Timestamp("2023-11-03"), "description": "Test 3"}
    ])


def test_get_cards_info(sample_df):
    result = get_cards_info(sample_df)
    assert len(result) == 2
    # Проверяем, что сумма посчиталась (1000+2000=3000)
    assert result[0]["total_spent"] == 3000.0 or result[1]["total_spent"] == 3000.0


def test_get_top_transactions(sample_df):
    result = get_top_transactions(sample_df)
    assert len(result) == 3
    # Первая должна быть на 2000
    assert result[0]["amount"] == 2000


# --- ТЕСТЫ ДЛЯ SERVICES ---

def test_simple_search(sample_df):
    result = simple_search(sample_df, "Test 2")
    assert len(result) == 1
    assert result[0]["amount"] == 2000


def test_simple_search_empty(sample_df):
    result = simple_search(sample_df, "")
    assert result == []


# --- ТЕСТЫ ДЛЯ UTILS (с моками) ---

@patch("src.utils.requests.get")
def test_get_currency_rates(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"Valute": {"USD": {"Nominal": 1, "Value": 90.0}}}

    result = get_currency_rates(["USD"])
    assert result == [{"currency": "USD", "rate": 90.0}]


@patch("src.utils.requests.get")
def test_get_stock_prices(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "chart": {"result": [{"meta": {"regularMarketPrice": 150.5}}]}
    }

    result = get_stock_prices(["AAPL"])
    assert result == [{"stock": "AAPL", "price": 150.5}]