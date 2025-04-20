import json
import logging
import os
from typing import Any, Dict, List

from make_log_dir import make_dir

make_dir()
default_logs_path_name = "../logs/utils.log"
filename = "..//exchangerates_data/currency_USD_EUR.json"

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(default_logs_path_name, mode="w")
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_path_to_json(directory: str = "..\\data", filename: str = "operations.json") -> List[Dict[str, Any]]:
    """Функция, которая принимает на вход путь до JSON-файла и
    возвращает список словарей с данными о финансовых транзакциях."""

    full_path = os.path.join(directory, filename)
    try:
        with open(full_path, "r", encoding="utf-8") as file:
            logger.debug("Load transaction data success")
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error: {e}")
        return []


def load_json(file_name: str) -> list[Any] | Any:
    """Функция загрузки данных из .json файла"""
    try:

        with open(file_name, "r", encoding="utf-8") as f:
            logger.debug("Load data success")
            data = json.load(f)
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error: {e}")
        return []


def get_sum_amount(dict_transactions: List[Dict[str, Any]]) -> float:
    """Функция, которая принимает на вход транзакцию и возвращает сумму всех транзакции в рублях"""

    rates_USD = load_json(filename)["rates"]["USD"]
    logger.debug("Load rates_USD success")
    rates_EUR = load_json(filename)["rates"]["EUR"]
    logger.debug("Load rates_EUR success")

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
    logger.info("Calculation  was completed successfully")

    return total_sum


# Проверка работы функции
# print(get_sum_amount(get_path_to_json()))
