import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import pandas as pd

from src.utils import get_transactions_read_excel

ROOTPATH = Path(__file__).resolve().parent.parent

logger = logging.getLogger("reports")
file_handler = logging.FileHandler(Path(ROOTPATH, "logs/reports.log"), "w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)"""

    if date is None:
        logger.info("Если не указана дата, то назначается дата последней транзакции '31.12.2021 16:44:00'")
        date = "31.12.2021 16:44:00"

    logger.info("DataFrame с транзакциями преобразовывается в список")
    transactions_list = transactions.to_dict(orient="records")
    logger.info("Определяется начальная дата")
    input_date = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    delta = timedelta(days=90)
    start_date = input_date - delta
    filter_list = []
    logger.info("Перебирается список в выбранном периоде и транзакция с заданной категорией добавляется в список")
    for transaction in transactions_list:
        date_transaction = datetime.strptime(str(transaction.get("Дата операции")), "%d.%m.%Y %H:%M:%S")
        if start_date <= date_transaction <= input_date:
            if str(transaction.get("Категория")).lower() == category.lower():
                filter_list.append(transaction)
    if not filter_list:
        logger.warning(f"Трат по заданной категории {category} за период {start_date} - {input_date} не найдено!")
        print(f"Трат по заданной категории {category} за период {start_date} - {input_date} не найдено!")
    logger.info("Список преобразуется обратно в DataFrame")
    result = pd.DataFrame(filter_list)
    return result


if __name__ == "__main__":
    file_p = Path(ROOTPATH, "data/operations.xlsx")
    transactions_l = get_transactions_read_excel(str(file_p))
    transactions_pd = pd.DataFrame(transactions_l)
    category_in = input("Введите категорию трат: ")
    result_pd = spending_by_category(transactions_pd, category_in)
    print(result_pd)
