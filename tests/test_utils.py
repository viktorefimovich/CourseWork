import json
from datetime import datetime
from pathlib import Path
from unittest.mock import patch, MagicMock

import pandas as pd
import pytest
import requests

from src.utils import get_transactions_read_excel, get_greeting, get_format_data, filter_by_date, get_info_cards, \
    get_rate, get_exchange_rates, get_stocks_cost, get_top_transactions

ROOTPATH = Path(__file__).resolve().parent.parent


def test_get_transactions_read_excel():
    test_data = [
        {
            "Дата операции": "01.06.2023 12:00:00",
            "Сумма операции": "-100.50",
            "Категория": "Покупки",
            "Описание": "Магазин"
        },
        {
            "Дата операции": "15.06.2023 18:30:00",
            "Сумма операции": "-250.00",
            "Категория": "Ресторан",
            "Описание": "Ужин"
        }
    ]

    file_path_test = str(ROOTPATH / "data/operations.xlsx")

    df = pd.DataFrame(test_data)

    with patch("pandas.read_excel", return_value=df):
        result = get_transactions_read_excel(file_path_test)
        assert result == test_data


@patch("src.utils.datetime")
@pytest.mark.parametrize(
    "current_hour, expected_greeting",
    [
        (7, "Доброе утро!"),
        (13, "Добрый день!"),
        (19, "Добрый вечер!"),
        (2, "Доброй ночи!")
    ]
)
def test_get_greeting(mock_datetime: MagicMock, current_hour: int, expected_greeting: str) -> None:
    mock_now = datetime(2023, 6, 20, current_hour, 0, 0)
    mock_datetime.now.return_value = mock_now
    result = get_greeting()
    assert result == expected_greeting


def test_get_format_data():
    date_str = "2022-01-01 00:00:00"
    expected_result = datetime(2022, 1, 1, 0, 0, 0)

    result = get_format_data(date_str)
    assert result == expected_result


@pytest.mark.parametrize(
    "input_date, expected_result",
    [
        (
            "2023-06-20 12:00:00",
            [
                {
                    "Дата операции": "01.06.2023 12:00:00",
                    "Сумма платежа": "-100.50",
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
                }
            ]
        ),
        (
            "2023-05-15 12:00:00",
            [
                {
                    "Дата операции": "05.05.2023 08:15:00",
                    "Сумма платежа": "-500.00",
                    "Категория": "Медицина",
                    "Описание": "Аптека"
                }
            ]
        )
    ]
)
def test_filter_by_date(test_transactions, input_date, expected_result):
    result = filter_by_date(test_transactions, input_date)
    assert result == expected_result


def test_get_info_cards():
    test_data = [
        {
            "Номер карты": "*1234",
            "Дата операции": "01.01.2024 12:00:00",
            "Сумма платежа": "-100",
            "Валюта платежа": "RUB"
        },
        {
            "Номер карты": "*1234",
            "Дата операции": "05.01.2024 12:00:00",
            "Сумма платежа": "-200",
            "Валюта платежа": "RUB"
        },
        {
            "Номер карты": "*1235",
            "Дата операции": "01.01.2024 12:00:00",
            "Сумма платежа": "-100",
            "Валюта платежа": "RUB"
        }
    ]
    result = get_info_cards(test_data)
    assert result == [
        {
            "last_digits": "1234",
            "total_spent": 300,
            "cashback": 3
        },
        {
            "last_digits": "1235",
            "total_spent": 100,
            "cashback": 1
        }
    ]


@patch("requests.request")
def test_get_rate(mock_request):

    rate = "USD"
    date_transaction = "2022-01-01"
    expected_result = {"currency": "USD", "rate": 70.0}

    response_json = json.loads('{"info":{"rate":70.0}}')
    mock_response = requests.models.Response()
    mock_response.status_code = 200
    mock_response._content = json.dumps(response_json).encode()
    mock_request.return_value = mock_response

    result = get_rate(rate, date_transaction)
    assert result == expected_result


@patch('requests.request')
def test_get_exchange_rates_success(mock_request):

    currencies = ["USD", "EUR"]
    expected_results = [
         {"currency": "USD", "rate": 70.0},
         {"currency": "EUR", "rate": 80.0}
    ]

    response_usd = json.loads('{"info":{"rate":70.0}}')
    response_eur = json.loads('{"info":{"rate":80.0}}')

    mock_response_usd = requests.models.Response()
    mock_response_usd.status_code = 200
    mock_response_usd._content = json.dumps(response_usd).encode()

    mock_response_eur = requests.models.Response()
    mock_response_eur.status_code = 200
    mock_response_eur._content = json.dumps(response_eur).encode()

    mock_request.side_effect = [mock_response_usd, mock_response_eur]

    result = get_exchange_rates(currencies)
    assert result == expected_results


@patch('requests.get')
def test_get_stocks_cost_success(mock_get):
    companies = ["AAPL", "MSFT"]
    expected_results = [
        {"stock": "AAPL", "price": 100.0},
        {"stock": "MSFT", "price": 50.0}
    ]

    response_aapl = json.loads('{"Time Series (Daily)":{"2024-01-01": {"4. close": 100.0}}}')
    response_msft = json.loads('{"Time Series (Daily)":{"2024-01-01": {"4. close": 50.0}}}')

    mock_response_aapl = requests.models.Response()
    mock_response_aapl.status_code = 200
    mock_response_aapl._content = json.dumps(response_aapl).encode()

    mock_response_msft = requests.models.Response()
    mock_response_msft.status_code = 200
    mock_response_msft._content = json.dumps(response_msft).encode()

    mock_get.side_effect = [mock_response_aapl, mock_response_msft]

    result = get_stocks_cost(companies)
    assert result == expected_results


def test_get_top_transactions():
    test_tran = [
        {
            "Дата операции": "01.06.2023 12:00:00",
            "Сумма платежа": "-100.50",
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
        }
    ]
    expected_result = [
        {
            "date": "2023-06-15",
            "amount": "-250.00",
            "category": "Ресторан",
            "description": "Ужин"
        },
        {
            "date": "2023-06-01",
            "amount": "-100.50",
            "category": "Покупки",
            "description": "Магазин"
        },
        {
            "date": "2023-06-20",
            "amount": "-75.00",
            "category": "Транспорт",
            "description": "Такси"
        }
    ]

    result = get_top_transactions(test_tran)
    assert result == expected_result
