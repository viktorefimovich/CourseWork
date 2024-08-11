import json
import pytest
from unittest.mock import patch
from src.views import home_page  # Импортируйте ваш модуль


@pytest.fixture
def mock_user_settings():
    return {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "GOOGL"]
    }


@pytest.fixture
def mock_transactions():
    return [
        {"date": "2024-08-01", "amount": 100},
        {"date": "2024-08-02", "amount": 150}
    ]


@pytest.fixture
def mock_filtered_transactions(mock_transactions):
    return mock_transactions  # В реальных тестах вы можете модифицировать это в зависимости от логики


@patch("src.views.get_info_cards", return_value=[{"card": "Visa", "balance": 1000}])
@patch("src.views.get_exchange_rates", return_value={"USD": 1.0, "EUR": 0.9})
@patch("src.views.get_stocks_cost", return_value={"AAPL": 150, "GOOGL": 2800})
@patch("src.views.get_greeting", return_value="Hello, User!")
@patch("src.views.get_top_transactions", return_value=[{"date": "2024-08-02", "amount": 150}])
@patch("src.views.get_transactions_read_excel")
@patch("src.views.filter_by_date")
@patch("src.views.user_settings", return_value={"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "GOOGL"]})
def test_home_page(mock_greeting, mock_transactions_read_excel, mock_filter_by_date,
                   mock_info_cards, mock_top_transactions, mock_exchange_rates,
                   mock_stocks_cost, mock_user_settings, mock_transactions, mock_filtered_transactions):
    # Настройка mock-объектов
    mock_transactions_read_excel.return_value = mock_transactions
    mock_filter_by_date.return_value = mock_filtered_transactions

    # Вызов тестируемой функции
    input_date = "2024-08-02 12:00:00"
    response = home_page(input_date)

    # Проверка результата
    expected_data = {
        "get_greeting": "Hello, User!",
        "cards": [{"card": "Visa", "balance": 1000}],
        "top_transactions": [{"date": "2024-08-02", "amount": 150}],
        "currency_rates": {"USD": 1.0, "EUR": 0.9},
        "stock_prices": {"AAPL": 150, "GOOGL": 2800}
    }
    assert json.loads(response) == expected_data
