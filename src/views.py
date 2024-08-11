import json
import logging
from pathlib import Path
from typing import Any

from src.utils import (
    filter_by_date,
    get_exchange_rates,
    get_greeting,
    get_info_cards,
    get_stocks_cost,
    get_top_transactions,
    get_transactions_read_excel,
)

ROOTPATH = Path(__file__).resolve().parent.parent

user_set_file = Path(ROOTPATH, "user_settings.json")
with open(user_set_file, "r") as file:
    user_settings = json.load(file)
file_path = str(ROOTPATH / "data/operations.xlsx")

logger = logging.getLogger("views")
file_handler = logging.FileHandler(Path(ROOTPATH, "logs/views.log"), "w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def home_page(input_date: str) -> Any:
    """
    Функция принимает на вход строку с датой и временем в формате 'YYYY-MM-DD HH:MM:SS' и
    возвращающает JSON-ответ с данными
    """

    greetings = get_greeting()
    logger.info("Создается приветствие")
    transactions = get_transactions_read_excel(file_path)
    logger.info("Создается список транзакций из xlsx-файла")
    filtered_transactions = filter_by_date(transactions, input_date)
    logger.info("Фильтруется список с начала месяца до введенной даты")
    cards_info = get_info_cards(filtered_transactions)
    logger.info("Создается список с информацией по каждой карте")
    top_transactions = get_top_transactions(filtered_transactions)
    logger.info("Сортируется список транзакций по сумме платежа")
    exchange_rate = get_exchange_rates(user_settings["user_currencies"])
    logger.info("Создается курс валют из списка юзера")
    stocks_cost = get_stocks_cost(user_settings["user_stocks"])
    logger.info("Создается список котировок акций и списка юзера")
    data = {
        "get_greeting": greetings,
        "cards": cards_info,
        "top_transactions": top_transactions,
        "currency_rates": exchange_rate,
        "stock_prices": stocks_cost,
    }
    logger.info("Создается список для преобразования в json-строку")
    logger.info("Записывается json-строка")
    return json.dumps(data, ensure_ascii=False)


# if __name__ == "__main__":
#     in_date = input("Введите дату в формате 'YYYY-MM-DD HH:MM:SS': ")
#     print(home_page(in_date))
