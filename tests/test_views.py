import json
from unittest.mock import patch, Mock

import pandas as pd
import pytest
from pandas import DataFrame

from src.views import home_page


@pytest.fixture
def mock_get_greeting():
    with patch("src.utils.get_greeting") as mock:
        mock.return_value = "Добрый день!"
        yield mock


@pytest.fixture
def mock_get_stocks_cost():
    with patch("src.utils.get_stocks_cost") as mock:
        mock.return_value = [{"stock": "AAPL", "price": 150.0}]
        yield mock


@pytest.fixture
def mock_get_exchange_rates():
    with patch("src.utils.get_exchange_rates") as mock:
        mock.return_value = [{"currency": "USD", "rate": 75.0}]
        yield mock


@pytest.fixture
def mock_get_top_transactions():
    with patch("src.utils.get_top_transactions") as mock:
        mock.return_value = [{
            "date": "2023-06-15",
            "amount": "-250.00",
            "category": "Ресторан",
            "description": "Ужин"
        },
            {
                "date": "2023-06-01",
                "amount": "-150.00",
                "category": "Покупки",
                "description": "Магазин"
            }]
        yield mock


@pytest.fixture
def mock_get_info_cards():
    with patch("src.utils.get_info_cards") as mock:
        mock.return_value = [{
            "last_digits": "1234",
            "total_spent": 400,
            "cashback": 4.0
        }]
        yield mock


@pytest.fixture
def mock_filter_by_date():
    with patch("src.utils.filter_by_date") as mock:
        mock.return_value = [{
            "Дата операции": "01.06.2023 12:00:00",
            "Сумма платежа": "-150.00",
            "Категория": "Покупки",
            "Описание": "Магазин"
        },
            {
                "Дата операции": "15.06.2023 18:30:00",
                "Сумма платежа": "-250.00",
                "Категория": "Ресторан",
                "Описание": "Ужин"
            }]
        yield mock


@pytest.fixture
def mock_get_transactions_read_excel():
    with patch("src.utils.get_transactions_read_excel") as mock:
        mock.return_value = [{
            "Дата операции": "01.06.2023 12:00:00",
            "Сумма платежа": "-150.00",
            "Категория": "Покупки",
            "Описание": "Магазин"
        },
            {
                "Дата операции": "15.06.2023 18:30:00",
                "Сумма платежа": "-250.00",
                "Категория": "Ресторан",
                "Описание": "Ужин"
            },
            {
                "Дата операции": "20.06.2023 10:00:00",
                "Сумма платежа": "-75.00",
                "Категория": "Транспорт",
                "Описание": "Такси"
            }]
        yield mock


# def test_main(mock_get_greeting, mock_get_stocks_cost, mock_get_exchange_rates, mock_get_top_transactions,
#               mock_get_info_cards,
#               mock_filter_by_date, mock_get_transactions_read_excel):
#     date = "2021-06-21 12:00:00"
#     result = home_page(date)
#     expected_test = {
#         "greeting": "Добрый вечер!",
#         "cards": [{"last_digits": "1234", "total_spent": 400, "cashback": 4.0}],
#         "top_transactions": [
#             {
#                 "date": "2023-06-15",
#                 "amount": "-250.00",
#                 "category": "Ресторан",
#                 "description": "Ужин"
#             },
#             {
#                 "date": "2023-06-01",
#                 "amount": "-150.00",
#                 "category": "Покупки",
#                 "description": "Магазин"
#             }
#         ],
#         "currency_rates": [{"currency": "USD", "rate": 75.0}],
#         "stock_prices": [{"stock": "AAPL", "price": 150.0}]
#     }
#     assert json.loads(result) == expected_test


@patch("pandas.read_excel")
def test_main(mock_reader: Mock):
    mock_reader.return_value = DataFrame([{
        "Дата операции": "01.06.2023 12:00:00",
        "Сумма платежа": "-150.00",
        "Категория": "Покупки",
        "Описание": "Магазин"
    },
        {
            "Дата операции": "15.06.2023 18:30:00",
            "Сумма платежа": "-250.00",
            "Категория": "Ресторан",
            "Описание": "Ужин"
        },
        {
            "Дата операции": "20.06.2023 10:00:00",
            "Сумма платежа": "-75.00",
            "Категория": "Транспорт",
            "Описание": "Такси"
        }])
    assert home_page("2021-06-21 12:00:00") == json.dumps({
        "greeting": "Добрый вечер!",
        "cards": [{"last_digits": "1234", "total_spent": 400, "cashback": 4.0}],
        "top_transactions": [
            {
                "date": "2023-06-15",
                "amount": "-250.00",
                "category": "Ресторан",
                "description": "Ужин"
            },
            {
                "date": "2023-06-01",
                "amount": "-150.00",
                "category": "Покупки",
                "description": "Магазин"
            }
        ],
        "currency_rates": [{"currency": "USD", "rate": 75.0}],
        "stock_prices": [{"stock": "AAPL", "price": 150.0}]
    })

    # @patch("src.utils.get_stocks_cost")
    # @patch("src.utils.get_exchange_rates")
    # @patch("src.utils.get_top_transactions")
    # @patch("src.utils.get_info_cards")
    # @patch("src.utils.filter_by_date")
    # @patch("src.utils.get_transactions_read_excel")
    # @patch("pandas.read_excel")
    # def test_home_page(mock_read_exel, mock_get_transactions_read_excel, mock_filter_by_date, mock_get_info_cards,
    #                    mock_get_top_transactions,
    #                    mock_get_exchange_rates, mock_get_stocks_cost):
    #     user_settings = {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}
    #     mock_get_transactions_read_excel.return_value.mock_read_exel.return_value = [
    #         {
    #             "Дата операции": "01.06.2023 12:00:00",
    #             "Сумма платежа": "-150.00",
    #             "Категория": "Покупки",
    #             "Описание": "Магазин"
    #         },
    #         {
    #             "Дата операции": "15.06.2023 18:30:00",
    #             "Сумма платежа": "-250.00",
    #             "Категория": "Ресторан",
    #             "Описание": "Ужин"
    #         },
    #         {
    #             "Дата операции": "20.06.2023 10:00:00",
    #             "Сумма платежа": "-75.00",
    #             "Категория": "Транспорт",
    #             "Описание": "Такси"
    #         }
    #     ]
    #     mock_filter_by_date.return_value = [
    #         {
    #             "Дата операции": "01.06.2023 12:00:00",
    #             "Сумма платежа": "-150.00",
    #             "Категория": "Покупки",
    #             "Описание": "Магазин"
    #         },
    #         {
    #             "Дата операции": "15.06.2023 18:30:00",
    #             "Сумма платежа": "-250.00",
    #             "Категория": "Ресторан",
    #             "Описание": "Ужин"
    #         }
    #
    #     ]
    #     mock_get_info_cards.return_value = [
    #         {
    #             "last_digits": "1234",
    #             "total_spent": 400,
    #             "cashback": 4.0
    #         }
    #     ]
    #     mock_get_top_transactions.return_value = [
    #         {
    #             "date": "2023-06-15",
    #             "amount": "-250.00",
    #             "category": "Ресторан",
    #             "description": "Ужин"
    #         },
    #         {
    #             "date": "2023-06-01",
    #             "amount": "-150.00",
    #             "category": "Покупки",
    #             "description": "Магазин"
    #         }
    #     ]
    #     mock_get_exchange_rates.return_value = [{"currency": "USD", "rate": 75.0}]
    #     mock_get_stocks_cost.return_value = [{"stock": "AAPL", "price": 150.0}]
    #     date = "2023-06-15 12:00:00"
    #     result = home_page(date)
    #
    #     expected = {
    #         "greeting": "Добрый вечер!",
    #         "cards": [{"last_digits": "1234", "total_spent": 400, "cashback": 4.0}],
    #         "top_transactions": [
    #             {
    #                 "date": "2023-06-15",
    #                 "amount": "-250.00",
    #                 "category": "Ресторан",
    #                 "description": "Ужин"
    #             },
    #             {
    #                 "date": "2023-06-01",
    #                 "amount": "-150.00",
    #                 "category": "Покупки",
    #                 "description": "Магазин"
    #             }
    #         ],
    #         "currency_rates": [{"currency": "USD", "rate": 75.0}],
    #         "stock_prices": [{"stock": "AAPL", "price": 150.0}]
    #     }
    #
    #     assert json.loads(result) == expected
