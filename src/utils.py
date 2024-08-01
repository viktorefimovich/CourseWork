import os
from datetime import datetime
from pathlib import Path

import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

ROOTPATH = Path(__file__).resolve().parent.parent
env_path = ROOTPATH / ".env"
load_dotenv(env_path)

apy_key = os.getenv("apikey")
apikey = os.getenv("API_key")


def get_transactions_read_excel(file_path: str) -> list[dict]:
    """Функция принимает путь до xlsx-файла и возвращает список словарей с транзакциями"""

    try:
        data_file = pd.read_excel(file_path)
        return data_file.to_dict(orient="records")
    except Exception as e:
        print(f"Ошибка {e}")
        return []


# if __name__ == "__main__":
#     file_p = Path(ROOTPATH, "data/operations.xlsx")
#     trans = get_transactions_read_excel(str(file_p))
#     for tran in trans:
#         print(tran)


def get_greeting() -> str:
    """Функция выводит приветствие соответственно времени суток"""

    current_time = datetime.now()
    if 6 <= current_time.hour < 12:
        return "Доброе утро!"
    elif 12 <= current_time.hour < 18:
        return "Добрый день!"
    elif 18 <= current_time.hour < 23:
        return "Добрый вечер!"
    else:
        return "Доброй ночи!"


# if __name__ == "__main__":
#     date_now = get_greeting()
#     print(date_now)


def get_format_data(date_str: str) -> datetime:
    """Функция преобразует дату из строки в формат datetime"""

    return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")


# if __name__ == "__main__":
#     date_input = "1984-12-21 17:45:00"
#     print(get_format_data(date_input))
#     print(type(get_format_data(date_input)))


def filter_by_date(transactions: list[dict], input_date: str) -> list[dict]:
    """Функция фильтрует транзакции с начала месяца до заданной даты"""

    input_date_temp = get_format_data(input_date)
    start_date = datetime(input_date_temp.year, input_date_temp.month, 1)
    filter_transactions = []
    for transaction in transactions:
        date_transaction = datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S")
        if start_date <= date_transaction <= input_date_temp:
            filter_transactions.append(transaction)

    return filter_transactions


# if __name__ == "__main__":
#     file_p = Path(ROOTPATH, "data/operations.xlsx")
#     trans = get_transactions_read_excel(str(file_p))
#     in_date = "2021-12-03 23:10:00"
#     f_trans = filter_by_date(trans, in_date)
#     for f_tran in f_trans:
#         print(f_tran)


def get_info_cards(transactions: list[dict]) -> list[dict]:
    """Функция принимает список транзакций и выдает список с информацией по каждой карте"""

    list_card = {}
    list_info_card = []
    for transaction in transactions:
        if not transaction.get("Номер карты"):
            continue

        card_number = transaction.get("Номер карты")[-4:]
        if card_number not in list_card:
            list_card[card_number] = {"total_spent": 0, "cashback": 0}

        if transaction.get("Валюта платежа") != "RUB":
            date_transaction = datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S")
            date_transaction = date_transaction.strftime("%Y-%m-%d")
            exchange_rate = get_rate(transaction.get("Валюта платежа"), date_transaction)
            amount = float(transaction.get("Сумма платежа")) * exchange_rate["rate"] / 100
        else:
            amount = float(transaction.get("Сумма платежа"))

        if amount < 0:
            list_card[card_number]["total_spent"] += abs(amount)
            list_card[card_number]["cashback"] += abs(amount) * 0.01
    for last_digits, data in list_card.items():
        list_info_card.append(
            {
                "last_digits": last_digits,
                "total_spent": round(data["total_spent"], 2),
                "cashback": round(data["cashback"], 2)
            }
        )
    return list_info_card


# if __name__ == "__main__":
#     file_p = Path(ROOTPATH, "data/operations.xlsx")
#     trans = get_transactions_read_excel(str(file_p))
#     in_date = "2021-12-01 23:59:59"
#     f_trans = filter_by_date(trans, in_date)
#     list_info = get_info_cards(f_trans)
#     for tran in list_info:
#         print(tran)


def get_rate(rate: str, date_transaction: str) -> dict:
    """Функция принимает код валюты, дату и возвращает словарь с курсом валюты"""
    exchange_rate = {}
    url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={rate}&amount=1&date={date_transaction}"
    payload = {}
    headers = {"apikey": apy_key}
    response = requests.request("get", url, headers=headers, data=payload)
    if response.status_code == 200:
        data = response.json()
        exchange_rate["currency"] = rate
        exchange_rate["rate"] = data["info"]["rate"]
    else:
        print(f"Ошибка: {response.status_code}, {response.text} !")
        exchange_rate = {"currency": rate, "rate": None}
    return exchange_rate


# if __name__ == "__main__":
#     in_date = "2024-07-31"
#     rate_str = "CNY"
#     dict_exchange = get_rate(rate_str, in_date)
#     print(dict_exchange)


def get_exchange_rates(currencies: list[str]) -> list[dict]:
    """Функция принимае список валюты и возвращает список курсов этих валют"""

    exchange_rates = []
    date_now = datetime.today()
    date_now = date_now.strftime("%Y-%m-%d")
    for currency in currencies:
        exchange_rates.append(get_rate(currency, date_now))
    return exchange_rates


# if __name__ == "__main__":
#     list_currency = ["USD", "EUR"]
#     list_exchange = get_exchange_rates(list_currency)
#     print(list_exchange)


def get_stocks_cost(companies: list[str]) -> list[dict]:
    """
    Функция принимает список тикеров компаний из индекса S&P500 и
    возвращает список словарей со стоимостью акций этих компаний
    """

    stocks_cost = []
    for company in companies:
        url = (f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&'
               f'symbol={company}&interval=5min&apikey={apikey}')
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            time_series = data.get("Time Series (5min)")
            if time_series:
                last_date = max(time_series.keys())
                last_data = time_series[last_date]
                stock_cost = last_data["4. close"]
                stocks_cost.append({"stock": company, "price": stock_cost})
            else:
                stocks_cost.append({"stock": company, "price": None})
        else:
            print(f"Ошибка: {response.status_code}, {response.text} !")
            stocks_cost.append({"stock": company, "price": None})
    return stocks_cost


# if __name__ == "__main__":
#     list_companies = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
#     list_stocks_cost = get_stocks_cost(list_companies)
#     for stock_company in list_stocks_cost:
#         print(stock_company)

