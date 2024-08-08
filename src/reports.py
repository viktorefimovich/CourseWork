import logging
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

# from src.utils import get_transactions_read_excel

ROOTPATH = Path(__file__).resolve().parent.parent

logger = logging.getLogger("reports")
file_handler = logging.FileHandler(Path(ROOTPATH, "logs/reports.log"), "w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def spending_by_category(transactions: pd.DataFrame, category: str, date: str | None = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)"""

    if not date:
        date = str(datetime.today()).rsplit(".", 1)[0]
        right_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    else:
        right_date = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")

    left_date = right_date - timedelta(days=90)

    df = transactions

    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    filtered_df = df.loc[(df["Дата операции"] >= left_date) & (df["Дата операции"] <= right_date)]
    filtered_df = filtered_df.loc[df["Категория"] == category]

    return filtered_df


# if __name__ == "__main__":
#     file_p = Path(ROOTPATH, "data/operations.xlsx")
#     transactions_l = get_transactions_read_excel(str(file_p))
#     transactions_pd = pd.DataFrame(transactions_l)
#     category_in = input("Введите категорию трат: ")
#     date_in = "31.12.2021 23:59:59"
#     result_pd = spending_by_category(transactions_pd, category_in, date_in)
#     print(result_pd)
