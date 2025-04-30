import csv
import json
import os
from typing import Union

import pandas as pd

path_to_file_json = "../data/operations.json"
path_to_file_csv = "../data/transactions.csv"
path_to_file_xls = "../data/transactions_excel.xlsx"


def read_file(path_to_file: str) -> Union[str, dict]:
    """Функция чтения данных из файлов формата .csv .xls .xlsx"""
    # Проверяем расширение файла
    extension = os.path.splitext(path_to_file)[1].lower()

    if extension == '.csv':
        try:
            sniffer = csv.Sniffer()
            with open(path_to_file, 'r') as fp:
                sample = fp.readline()
                try:
                    delimiter_csv = sniffer.sniff(sample).delimiter
                except:
                    delimiter_csv = ','
                fp.seek(0)  # Возврат указателя в начало строки
            df = pd.read_csv(path_to_file, delimiter=delimiter_csv)
        except Exception as e:
            return f"Ошибка при чтении CSV: {str(e)}"

    elif extension in ('.xlsx', '.xls'):
        try:
            df = pd.read_excel(path_to_file)
        except Exception as e:
            return f"Ошибка при чтении Excel: {str(e)}"

    elif extension == '.json':
        try:
            with open(path_to_file, "r", encoding="utf-8") as file:
                data = json.load(file)
            return json.dumps(data, indent=4)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            return f"Ошибка при чтении .json: {str(e)}"

    else:
        return "Укажите файл с расширением .csv, .xlsx/.xls или .json"

    if df.empty:
        return "Файл не содержит данных"

    # Конвертируем в JSON
    try:
        json_data = df.to_json(orient='records', indent=4)
        return json_data
    except Exception as e:
        return f"Ошибка при конвертации в JSON: {str(e)}"


# Проверка работы функции
# print(read_file(path_to_file_csv))
# print(read_file(path_to_file_xls))
# print(read_file(path_to_file_json))
