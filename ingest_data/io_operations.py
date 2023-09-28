import json
import pandas as pd


def read_excel_data(filename: str, sheet_name: str) -> pd.DataFrame:
    return pd.read_excel(filename, sheet_name=sheet_name)


def write_to_json(data: dict, filename: str):
    with open(filename, 'w') as f:
        json.dump(data, f)
