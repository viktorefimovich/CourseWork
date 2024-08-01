import json
from pathlib import Path
from typing import Any

from utils import (
    get_transactions_read_excel,
    filter_by_date, get_info_cards,
    get_top_transactions,
    get_exchange_rates,
    get_stocks_cost,
    get_greeting
)

ROOTPATH = Path(__file__).resolve().parent.parent

user_set_file = Path(ROOTPATH, "user_settings.json")
with open(user_set_file, "r") as file:
    user_settings = json.load(file)
file_path = str(ROOTPATH / "data/operations.xlsx")


def home_page(input_date: str) -> Any:
    """
    Функция принимает на вход строку с датой и временем в формате 'YYYY-MM-DD HH:MM:SS' и
    возвращающает JSON-ответ с данными
    """

    greetings = get_greeting()
    transactions = get_transactions_read_excel(file_path)
    filtered_transactions = filter_by_date(transactions, input_date)
    cards_info = get_info_cards(filtered_transactions)
    top_transactions = get_top_transactions(filtered_transactions)
    exchange_rate = get_exchange_rates(user_settings["user_currencies"])
    stocks_cost = get_stocks_cost(user_settings["user_stocks"])
    data = {"get_greeting": greetings, "cards": cards_info, "top_transactions": top_transactions,
            "currency_rates": exchange_rate, "stock_prices": stocks_cost}

    return json.dumps(data, ensure_ascii=False)


if __name__ == "__main__":
    in_date = input("Введите дату в формате 'YYYY-MM-DD HH:MM:SS': ")
    print(home_page(in_date))
