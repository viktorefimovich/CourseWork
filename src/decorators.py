import os
from functools import wraps
from pathlib import Path
from typing import Callable

import pandas as pd

ROOTPATH = Path(__file__).resolve().parent.parent


def to_excel(file_name: str = "result_{func}.xls") -> Callable:
    """
    Декоратор для сохранения результатов в файл.
    :param file_name: Имя файла в которую будет сохранён результат. По умолчанию result_ИмяФункции.xls
    :return: Результат работы функции
    """

    def wrapper(func: Callable) -> Callable:
        @wraps(func)
        def inner(*args: tuple, **kwargs: dict) -> pd.DataFrame:

            result: pd.DataFrame = func(*args, **kwargs)

            result.to_excel(
                 f"{os.path.join(ROOTPATH, file_name.format(func=func.__name__))}", index=False, engine="openpyxl"
            )

            return result

        return inner

    return wrapper


# def my_decorator(file_name: str = f"report_function.txt"):
#     def wrapper(func):
#         def inner(*args, **kwargs):
#             result = func(*args, **kwargs)
#             with open(Path(ROOTPATH, file_name), "w") as file:
#                 file.write(result)
#             return result
#         return inner
#
#     return wrapper
