import csv
import json
import os
from typing import Union, List, Dict

import pandas as pd


def read_file(path_to_file: str) -> Union[str, List[Dict]]:
    """Функция чтения данных из файлов формата .csv, .xls, .xlsx, .json"""


    if not os.path.exists(path_to_file):
        return f"Файл не найден: {path_to_file}"

    extension = os.path.splitext(path_to_file)[1].lower()

    # Обработка JSON файлов
    if extension == '.json':
        try:
            with open(path_to_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                if not data:  # Проверка на пустые данные
                    return "Файл не содержит данных"
                return data
        except (FileNotFoundError, json.JSONDecodeError) as e:
            return f"Ошибка при чтении JSON: {str(e)}"
        except Exception as e:
            return f"Неожиданная ошибка при чтении JSON: {str(e)}"

    # Обработка CSV/Excel файлов
    elif extension in ('.csv', '.xlsx', '.xls'):
        try:
            if extension == '.csv':
                # Автоопределение разделителя
                with open(path_to_file, 'r') as fp:
                    sample = fp.readline()
                    try:
                        delimiter = csv.Sniffer().sniff(sample).delimiter
                    except:
                        delimiter = ','
                    # Возврат указателя в начало строки
                    fp.seek(0)
                df = pd.read_csv(path_to_file, delimiter=delimiter)
            else:
                df = pd.read_excel(path_to_file)

            if df.empty:
                return "Файл не содержит данных"

            # Конвертируем DataFrame в список словарей
            return df.to_dict('records')

        except Exception as e:
            return f"Ошибка при чтении {extension.upper()}: {str(e)}"

    else:
        return "Поддерживаются только файлы .csv, .xlsx/.xls или .json"