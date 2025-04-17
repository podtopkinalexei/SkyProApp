import json
import os
from typing import Any, Dict, List, Union

from src.external_api import get_currency_rate

# Загружаем курсы валют
get_currency_rate()

# Расположение файла с курсами валют
directory_currency = "..//exchangerates_data"
filename_currency = "currency_USD_EUR.json"

# Расположение файла с операциями
directory_operations = "..//data"
filename_operation = "operations.json"


def get_sum_amount(directory: str = "..//data", filename: str = "operations.json") -> float:
    """Функция, которая принимает на вход путь к файлу с транзакциями и возвращает сумму всех транзакций в рублях"""

    def load_json(directory: str, filename: str) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """Функция загрузки данных из .json файла.

        Возвращает:
            - список словарей для файла операций
            - словарь для файла с курсами валют
            - пустой список в случае ошибки
        """
        full_path = os.path.join(directory, filename)
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except (FileNotFoundError, json.JSONDecodeError) as e:
            return []

    # Определяем курс валют
    currency_data: Dict[str, Any] = load_json(directory_currency, filename_currency)
    if not currency_data or "rates" not in currency_data:
        raise ValueError("Не удалось загрузить данные о курсах валют")
    rates_USD: float = currency_data["rates"]["USD"]
    rates_EUR: float = currency_data["rates"]["EUR"]

    # Осуществляем расчет
    dict_transactions: List[Dict[str, Any]] = load_json(directory_operations, filename_operation)
    if not isinstance(dict_transactions, list):
        raise ValueError("Ожидается список транзакций")

    rub_sum: float = round(sum(
        float(transactions["operationAmount"]["amount"])
        for transactions in dict_transactions
        if "operationAmount" in transactions
        and transactions["operationAmount"]["currency"]["code"] == "RUB"
    ), 2)

    sum_usd: float = round(sum(
        float(transactions["operationAmount"]["amount"])
        for transactions in dict_transactions
        if "operationAmount" in transactions
        and transactions["operationAmount"]["currency"]["code"] == "USD"
    ), 2)

    sum_eur: float = round(sum(
        float(transactions["operationAmount"]["amount"])
        for transactions in dict_transactions
        if "operationAmount" in transactions
        and transactions["operationAmount"]["currency"]["code"] == "EUR"
    ), 2)

    total_sum: float = round(rub_sum + (sum_usd * rates_USD) + (sum_eur * rates_EUR), 2)

    return total_sum
