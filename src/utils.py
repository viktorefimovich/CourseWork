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
