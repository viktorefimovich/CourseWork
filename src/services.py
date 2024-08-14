import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

# from utils import get_transactions_read_excel

ROOTPATH = Path(__file__).resolve().parent.parent

logger = logging.getLogger("services")
file_handler = logging.FileHandler(Path(ROOTPATH, "logs/services.log"), "w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def investment_bank(filtered_month: str, transactions_list: List[Dict[str, Any]], limit: int) -> float:
    """Функция возвращает сумму, которую удалось бы отложить в Инвесткопилку за введенный месяц"""

    total_amount: float = 0
    logger.info("Проверяется дата каждой транзакции на вхождение в введенный месяц")
    for transaction in transactions_list:
        transaction_date = datetime.strptime(str(transaction.get("Дата операции")), "%d.%m.%Y %H:%M:%S")
        if transaction_date.strftime("%Y-%m") == filtered_month:
            if float(str(transaction.get("Сумма платежа"))) < 0:
                remain = abs(float(str(transaction.get("Сумма платежа")))) % limit
                if remain == 0:
                    continue
                else:
                    total_amount = total_amount + (limit - remain)
    logger.info("Возвращается сумма Инвесткопилки")
    return total_amount


# if __name__ == "__main__":
#     input_month = input("Введите месяц и год в формате 'YYYY-MM': ")
#     file_p = Path(ROOTPATH, "data/operations.xlsx")
#     transactions = get_transactions_read_excel(str(file_p))
#     round_limit = int(input("Введите предел округления: "))
#     result = investment_bank(input_month, transactions, round_limit)
#     print(f"Сумма, которую удалось бы отложить в 'Инвесткопилку' за {input_month} равняется: {result}")
