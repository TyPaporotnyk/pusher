import pandas as pd


def get_excel_file_not_contains_columns(file, columns: list[str]) -> list[str]:
    df = pd.read_excel(file)
    return [column for column in columns if column not in df.columns]
