from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import pandas as pd

from src.utils import get_transactions_read_excel

ROOTPATH = Path(__file__).resolve().parent.parent


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)"""

    if date is None:
        date = "31.12.2021 16:44:00"

    transactions_list = transactions.to_dict(orient="records")
    input_date = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    delta = timedelta(days=90)
    start_date = input_date - delta
    filter_list = []
    for transaction in transactions_list:
        date_transaction = datetime.strptime(str(transaction.get("Дата операции")), "%d.%m.%Y %H:%M:%S")
        if start_date <= date_transaction <= input_date:
            if str(transaction.get("Категория")).lower() == category.lower():
                filter_list.append(transaction)
    if not filter_list:
        print(f"Трат по заданной категории {category} за период {start_date} - {input_date} не найдено!")
    result = pd.DataFrame(filter_list)
    return result


if __name__ == "__main__":
    file_p = Path(ROOTPATH, "data/operations.xlsx")
    transactions_l = get_transactions_read_excel(str(file_p))
    transactions_pd = pd.DataFrame(transactions_l)
    category_in = input("Введите категорию трат: ")
    result_pd = spending_by_category(transactions_pd, category_in)
    print(result_pd)
