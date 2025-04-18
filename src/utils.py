import json
import os
from typing import List, Dict, Any

from make_log_dir import make_dir

make_dir()
filename = "..//exchangerates_data/currency_USD_EUR.json"



def get_path_to_json(directory: str = "..\\data", filename: str = "operations.json") -> List[Dict[str, Any]]:
    """Функция, которая принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях."""

    full_path = os.path.join(directory, filename)
    try:
        with open(full_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return []


def load_json(file_name: str) -> list[Any] | Any:
    """Функция загрузки данных из .json файла"""
    try:

        with open(file_name, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return []


def get_sum_amount(dict_transactions: List[Dict[str, Any]]) -> float:
    """Функция, которая принимает на вход транзакцию и возвращает сумму всех транзакции в рублях"""

    rates_USD = load_json(filename)["rates"]["USD"]
    rates_EUR = load_json(filename)["rates"]["EUR"]

    rub_sum = round(sum(float(transactions["operationAmount"]["amount"]) for transactions in dict_transactions if
                        "operationAmount" in transactions and transactions["operationAmount"]["currency"][
                            "code"] == "RUB"), 2)

    sum_usd = round(sum(float(transactions["operationAmount"]["amount"]) for transactions in dict_transactions if
                        "operationAmount" in transactions and transactions["operationAmount"]["currency"][
                            "code"] == "USD"), 2)

    sum_eur = round(sum(float(transactions["operationAmount"]["amount"]) for transactions in dict_transactions if
                        "operationAmount" in transactions and transactions["operationAmount"]["currency"][
                            "code"] == "EUR"), 2)

    total_sum = round(rub_sum + (sum_usd * rates_USD) + (sum_eur * rates_EUR), 2)

    return total_sum



# Проверка работы функции
# print(get_sum_amount(get_path_to_json()))
