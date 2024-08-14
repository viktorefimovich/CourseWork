import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

ROOTPATH = Path(__file__).resolve().parent.parent
env_path = ROOTPATH / ".env"
load_dotenv(env_path)

apy_key = os.getenv("APIKEY")
apikey = os.getenv("API_KEY")

logger = logging.getLogger("utils")
file_handler = logging.FileHandler(Path(ROOTPATH, "logs/utils.log"), "w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def get_transactions_read_excel(file_path: str) -> list[dict]:
    """Функция принимает путь до xlsx-файла и возвращает список словарей с транзакциями"""

    try:
        logger.info("Записавается информация из xlsx-файла в датафрейм")
        data_file = pd.read_excel(file_path)
        logger.info("Создается список из датафрейма")
        return data_file.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Ошибка {e}")
        return []


# if __name__ == "__main__":
#     file_p = Path(ROOTPATH, "data/operations.xlsx")
#     trans = get_transactions_read_excel(str(file_p))
#     for tran in trans:
#         print(tran)


def get_greeting() -> str:
    """Функция выводит приветствие соответственно времени суток"""

    logger.info("Записывается настоящее время для определения времени суток")
    current_time = datetime.now()
    logger.info("Возвращается приветствие согласно времени суток")
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

    logger.info("Преобразуется формат времени из строки в объект datetime")
    return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")


# if __name__ == "__main__":
#     date_input = "1984-12-21 17:45:00"
#     print(get_format_data(date_input))
#     print(type(get_format_data(date_input)))


def filter_by_date(transactions: list[dict], input_date: str) -> list[dict]:
    """Функция фильтрует транзакции с начала месяца до заданной даты"""

    logger.info("Преобразование времени")
    input_date_temp = get_format_data(input_date)
    logger.info("Задается начальная дата")
    start_date = datetime(input_date_temp.year, input_date_temp.month, 1)
    logger.info("Создается пустой список")
    filter_transactions = []
    logger.info("Фильтруется список согласно введенной дате")
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


def get_info_cards(transactions: List[dict]) -> List[dict]:
    """Функция принимает список транзакций и выдает список с информацией по каждой карте"""

    logger.info("Создается пустой словарь для информации по карте")
    list_card = {}
    logger.info("Создается пустой список для информации по картам")
    list_info_card = []
    logger.info("Создается словарь с информацией по каждой карте")
    for transaction in transactions:
        if not transaction.get("Номер карты") or str(transaction.get("Номер карты")).strip().lower() == "nan":
            logger.warning("В транзакции отсутствует номер карты")
            continue

        card_number = str(transaction.get("Номер карты"))[-4:]
        if card_number not in list_card:
            logger.info("Записывается новая карта с информацией в словать")
            list_card[card_number] = {"total_spent": 0, "cashback": 0}

        if transaction.get("Валюта платежа") != "RUB":
            logger.info(f"Расчитывается сумма платежа из {transaction.get("Валюта платежа")} в 'RUB'")
            date_transaction_str = datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S")
            date_transaction = date_transaction_str.strftime("%Y-%m-%d")
            exchange_rate = get_rate(str(transaction.get("Валюта платежа")), date_transaction)
            amount = float(str(transaction.get("Сумма платежа"))) * exchange_rate["rate"] / 100
        else:
            amount = float(str(transaction.get("Сумма платежа")))

        if amount < 0:
            list_card[card_number]["total_spent"] += abs(amount)
            list_card[card_number]["cashback"] += abs(amount) * 0.01
    logger.info("Добавляются в список карты с необходимой информацией")
    for last_digits, data in list_card.items():
        list_info_card.append(
            {
                "last_digits": last_digits,
                "total_spent": round(data["total_spent"], 2),
                "cashback": round(data["cashback"], 2),
            }
        )
    return list_info_card


# if __name__ == "__main__":
#     file_p = Path(ROOTPATH, "data/operations.xlsx")
#     trans = get_transactions_read_excel(str(file_p))
#     in_date = "2021-12-31 23:59:59"
#     f_trans = filter_by_date(trans, in_date)
#     list_info = get_info_cards(f_trans)
#     for tran in list_info:
#         print(tran)


def get_rate(rate: str, date_transaction: Any) -> Dict:
    """Функция принимает код валюты, дату и возвращает словарь с курсом валюты"""

    logger.info("Создается пустой словарь для курса валюты")
    exchange_rate = {}
    url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={rate}&amount=1&date={date_transaction}"
    payload: dict[Any, Any] = {}
    headers = {"apikey": apy_key}
    logger.info("Происходит запрос курса валюты")
    response = requests.request("get", url, headers=headers, data=payload)
    if response.status_code == 200:
        logger.info("Успешный запрос преобразуется в словарь")
        data = response.json()
        exchange_rate["currency"] = rate
        exchange_rate["rate"] = data["info"]["rate"]
    else:
        logger.error(f"Произошла ошибка {response.status_code}, {response.text}")
        print(f"Ошибка: {response.status_code}, {response.text} !")
        exchange_rate = {"currency": rate, "rate": ""}
    return exchange_rate


# if __name__ == "__main__":
#     in_date = "2024-07-31"
#     rate_str = "CNY"
#     dict_exchange = get_rate(rate_str, in_date)
#     print(dict_exchange)


def get_exchange_rates(currencies: list[str]) -> list[dict]:
    """Функция принимае список валюты и возвращает список курсов этих валют"""

    logger.info("Создается пустой список для курсов валют")
    exchange_rates = []
    logger.info("Преобразуется и записывается настоящее время для запроса курса валюты")
    date_now_datetime = datetime.today()
    date_now = date_now_datetime.strftime("%Y-%m-%d")
    logger.info("В список добавляются курсы валюты из списка юзера")
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

    logger.info("Создается пустой список для котировок акций")
    stocks_cost = []
    logger.info("Делается запрос котировок согласно списку юзера и записывается в список")
    for company in companies:
        url = (
            f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&"
            f"symbol={company}&interval=5min&apikey={apikey}"
        )
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            time_series = data.get("Time Series (Daily)")
            if time_series:
                last_date = max(time_series.keys())
                last_data = time_series[last_date]
                stock_cost = last_data["4. close"]
                stocks_cost.append({"stock": company, "price": stock_cost})
            else:
                logger.error("Ошибка!")
                stocks_cost.append({"stock": company, "price": None})
        else:
            logger.error(f"Ошибка {response.status_code}, {response.text}")
            print(f"Ошибка: {response.status_code}, {response.text} !")
            stocks_cost.append({"stock": company, "price": None})
    return stocks_cost


# if __name__ == "__main__":
#     list_companies = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
#     list_stocks_cost = get_stocks_cost(list_companies)
#     for stock_company in list_stocks_cost:
#         print(stock_company)


def get_top_transactions(transactions: list[dict]) -> list[dict]:
    """Функция принимает список транзакций и выдает топ 5 транзакций по сумме платежа"""

    logger.info("Сортировка списка транзакций по сумме платежа")
    sorted_transactions = sorted(transactions, key=lambda x: abs(float(x["Сумма платежа"])), reverse=True)
    top_transactions = []
    logger.info("Создание топ-5 списка с необходимой информацией")
    for transaction in sorted_transactions[:5]:
        date_transaction = str(datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S").date())
        top_transactions.append(
            {
                "date": date_transaction,
                "amount": transaction["Сумма платежа"],
                "category": transaction["Категория"],
                "description": transaction["Описание"],
            }
        )
    return top_transactions


# if __name__ == "__main__":
#     file_p = Path(ROOTPATH, "data/operations.xlsx")
#     trans = get_transactions_read_excel(str(file_p))
#     in_date = "2021-12-02 23:59:59"
#     f_trans = filter_by_date(trans, in_date)
#     top_tr = get_top_transactions(f_trans)
#     for tran in top_tr:
#         print(tran)
