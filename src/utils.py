import json
import logging
from typing import Any, Dict, List

from make_log_dir import make_dir
from read_file import read_file

make_dir()
default_logs_path_name = "../logs/utils.log"
path_to_currency = "../exchangerates_data/currency_USD_EUR.json"

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(default_logs_path_name, mode="w")
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_sum_amount(dict_transactions: List[Dict[str, Any]]) -> float:
    """Функция, которая принимает на вход транзакцию и возвращает сумму всех транзакции в рублях"""

    data_currency = json.loads(read_file(path_to_currency))
    data_transactions = json.loads(dict_transactions)

    rates_USD = data_currency["rates"]["USD"]
    logger.debug("Load rates_USD success")
    rates_EUR = data_currency["rates"]["EUR"]
    logger.debug("Load rates_EUR success")

    rub_sum = round(
        sum(
            float(transactions["operationAmount"]["amount"])
            for transactions in data_transactions
            if "operationAmount" in transactions
            and transactions["operationAmount"]["currency"]["code"] == "RUB"
        ),
        2,
    )

    sum_usd = round(
        sum(
            float(transactions["operationAmount"]["amount"])
            for transactions in data_transactions
            if "operationAmount" in transactions
            and transactions["operationAmount"]["currency"]["code"] == "USD"
        ),
        2,
    )

    sum_eur = round(
        sum(
            float(transactions["operationAmount"]["amount"])
            for transactions in data_transactions
            if "operationAmount" in transactions
            and transactions["operationAmount"]["currency"]["code"] == "EUR"
        ),
        2,
    )

    total_sum = round(rub_sum + (sum_usd * rates_USD) + (sum_eur * rates_EUR), 2)
    logger.info("Calculation  was completed successfully")

    return total_sum


# Проверка работы функции
path_to_file_json = "../data/operations.json"
path_to_file_csv = "../data/transactions.csv"
path_to_file_xls = "../data/transactions_excel.xlsx"


data_ = read_file(path_to_file_json)

print(get_sum_amount(data_))
