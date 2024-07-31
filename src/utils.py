from datetime import datetime
from pathlib import Path

import pandas as pd

ROOTPATH = Path(__file__).resolve().parent.parent


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
