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


def get_transactions_read_excel(file_path: str) -> list[dict]:
    """Функция принимает путь до xlsx-файла и возвращает список словарей с транзакциями"""

    try:
        data_file = pd.read_excel(file_path)
        return data_file.to_dict(orient="records")
    except Exception as e:
        print(f"Ошибка {e}")
        return []


def get_greeting() -> str:
    """Функция выводит приветствие соответственно времени суток"""

    current_time = datetime.datetime.now()
    if 6 <= current_time.hour < 12:
        return "Доброе утро!"
    elif 12 <= current_time.hour < 18:
        return "Добрый день!"
    elif 18 <= current_time.hour < 23:
        return "Добрый вечер!"
    else:
        return "Доброй ночи!"


def get_format_data(data_str: str) -> datetime:
    """Функция преобразует дату из строки в формат datetime"""

    return datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")


def filter_by_date(transactions: list[dict], input_date: str) -> list[dict]:
    """Функция фильтрует транзакции с начала месяца до заданной даты"""

    input_date_temp = datetime.strptime(input_date, "%d.%m.%Y")
    start_date = datetime(input_date_temp.year, input_date_temp.month, 1)

    filter_transactions = [transaction for transaction in transactions if
                           start_date <= get_format_data(transaction["Дата операции"]) <= input_date_temp]
    return filter_transactions


def get_info_cards(transactions: list[dict]) -> list[dict]:
    list_card = {}
    list_info_card = []
    for transaction in transactions:
        if not transaction.get("Номер карты"):
            continue

        card_number = transaction.get("Номер карты")[-4:]
        if card_number not in list_card:
            list_card[card_number] = {"total_spent": 0, "cashback": 0}

        if transaction.get("Валюта платежа") != "RUB":
            date_transaction = datetime.strftime(get_format_data(transaction["Дата операции"]), "%Y-%m-%d")
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


def get_rate(rate: str, date_transaction: str) -> dict:
    exchange_rate = {}
    url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={rate}&amount=1&date={date_transaction}"
    payload = {}
    headers = {
        "apykey": apy_key
    }
    response = requests.request("get", url, headers=headers, data=payload)
    if response.status_code == 200:
        data = response.json()
        exchange_rate["currency"] = rate
        exchange_rate["rate"] = data["info"]["rate"]
    else:
        print(f"Ошибка: {response.status_code}, {response.text} !")
        exchange_rate = {"currency": rate, "rate": None}
    return exchange_rate
