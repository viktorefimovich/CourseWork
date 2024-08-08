import os
from pathlib import Path

import pandas as pd

from src.decorators import to_excel

ROOTPATH = Path(__file__).resolve().parent.parent


def test_deco():

    @to_excel()
    def some_func():
        return pd.DataFrame({"Test01": [0], "Test02": [1]})

    some_func()
    created_file_path = Path(ROOTPATH, "result_some_func.xls")
    assert os.path.exists(created_file_path)
    assert pd.read_excel(created_file_path).to_dict(orient="records") == [{"Test01": 0, "Test02": 1}]
    os.remove(created_file_path)
    assert not os.path.exists(created_file_path)
