from typing import Any, Dict, Iterator


def filter_by_currency(
    transactions: list[Dict[str, Any]], select_currency: str = "RUB"
) -> Iterator[Dict[str, Any]]:
    """Функция возвращает итератор, который поочередно выдает транзакции,
    где валюта операции соответствует заданной."""

    for operation in transactions:
        if (
            operation.get("operationAmount", {}).get("currency", {}).get("code")
            == select_currency
        ):
            yield operation


def transaction_descriptions(transactions: list[Dict[str, Any]]) -> Iterator[str]:
    """Функция принимает список словарей с транзакциями и возвращает описание каждой операции по очереди."""

    for operation in transactions:
        yield operation.get("description", "")


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """Функция генерирует номер банковской карты в заданном диапазоне в формате XXXX XXXX XXXX XXXX,
    где X — цифра номера карты."""

    checks = [
        isinstance(start, int),  # Проверка, что start — целое число
        isinstance(end, int),  # Проверка, что end — целое число
        0 <= start <= 9999999999999999,  # Проверка диапазона для start
        0 <= end <= 9999999999999999,  # Проверка диапазона для end
        start <= end,  # Проверка, что start не больше end
    ]

    if all(checks):
        gen_number = [f"{number:016d}" for number in range(start, end + 1)]

        for number in gen_number:
            yield f"{number[:4]} {number[4:8]} {number[8:12]} {number[12:16]}"
    else:
        print("Incorrect range")
