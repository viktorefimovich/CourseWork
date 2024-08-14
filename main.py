import pandas as pd

from src.reports import spending_by_category
from src.services import investment_bank
from src.utils import get_transactions_read_excel
from src.views import home_page

if __name__ == "__main__":

    print("\nПример работы функции для 'Веб-страницы' - 'Главная':\n")

    input_date = "2021-12-02 23:00:00"
    print("JSON-ответ функции: \n", home_page(input_date))

    print("\nПример работы функции для 'Сервисы' - Инвесткопилка:\n")

    transactions = get_transactions_read_excel("data/operations.xlsx")
    limit = 50
    print(investment_bank("2021-12", transactions, limit))

    print("\nПример работы функции для 'Отчеты' - 'Траты по категории':\n")
    transactions_df = pd.DataFrame(transactions)
    category = "Супермаркеты"
    date = "31.12.2021 23:59:59"
    print(spending_by_category(transactions_df, category, date))
