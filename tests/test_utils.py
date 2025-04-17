import json
import os
from unittest.mock import patch, mock_open

import pytest

from src.utils import get_sum_amount


@pytest.fixture
def mock_currency_data():
    return {
        "success": True,
        "timestamp": 1744885804,
        "base": "RUB",
        "date": "2025-04-17",
        "rates": {
            "USD": 0.012158,
            "EUR": 0.010691
        }
    }


@pytest.fixture
def mock_operations_data():
    return [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {
                "amount": "31957.58",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589"
        }
    ]


def test_get_sum_amount_success(mock_currency_data, mock_operations_data):

    # Используем side_effect для разных файлов
    with patch("builtins.open", side_effect=[
        mock_open(read_data=json.dumps(mock_currency_data)).return_value,
        mock_open(read_data=json.dumps(mock_operations_data)).return_value
    ]):
        result = get_sum_amount()

    # Проверяем правильность расчета (только RUB операция)
    assert result == 31957.58


def test_get_sum_amount_multiple_currencies(mock_currency_data):
    # Тест с операциями в разных валютах
    operations_data = [
        {
            "operationAmount": {
                "amount": "1000.00",
                "currency": {
                    "code": "RUB"
                }
            }
        },
        {
            "operationAmount": {
                "amount": "50.00",
                "currency": {
                    "code": "USD"
                }
            }
        },
        {
            "operationAmount": {
                "amount": "30.00",
                "currency": {
                    "code": "EUR"
                }
            }
        }
    ]


    with patch("builtins.open", side_effect=[
        mock_open(read_data=json.dumps(mock_currency_data)).return_value,
        mock_open(read_data=json.dumps(operations_data)).return_value
    ]):
        result = get_sum_amount()

    # Проверяем расчет
    expected = 1000.00 + (50.00 * 0.012158) + (30.00 * 0.010691)
    assert round(result, 2) == round(expected, 2)


def test_get_sum_amount_empty_operations(mock_currency_data):
    # Тест с пустым списком операций
    currency_path = os.path.join("..//exchangerates_data", "currency_USD_EUR.json")
    operations_path = os.path.join("..//data", "operations.json")

    with patch("builtins.open", side_effect=[
        mock_open(read_data=json.dumps(mock_currency_data)).return_value,
        mock_open(read_data=json.dumps([])).return_value
    ]):
        result = get_sum_amount()

    assert result == 0.00


def test_get_sum_amount_missing_currency_file():
    # Тест с отсутствующим файлом курсов валют
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(ValueError, match="Не удалось загрузить данные о курсах валют"):
            get_sum_amount()


def test_get_sum_amount_invalid_currency_data():
    # Тест с некорректными данными курсов валют (без ключа 'rates')
    invalid_currency_data = {"data": {}}
    currency_path = os.path.join("..//exchangerates_data", "currency_USD_EUR.json")
    operations_path = os.path.join("..//data", "operations.json")

    with patch("builtins.open", side_effect=[
        mock_open(read_data=json.dumps(invalid_currency_data)).return_value,
        mock_open(read_data=json.dumps([])).return_value
    ]):
        with pytest.raises(ValueError, match="Не удалось загрузить данные о курсах валют"):
            get_sum_amount()


def test_get_sum_amount_invalid_operations_data(mock_currency_data):
    # Тест с некорректными данными операций (не список)
    invalid_operations_data = {"operation": "invalid"}
    currency_path = os.path.join("..//exchangerates_data", "currency_USD_EUR.json")
    operations_path = os.path.join("..//data", "operations.json")

    with patch("builtins.open", side_effect=[
        mock_open(read_data=json.dumps(mock_currency_data)).return_value,
        mock_open(read_data=json.dumps(invalid_operations_data)).return_value
    ]):
        with pytest.raises(ValueError, match="Ожидается список транзакций"):
            get_sum_amount()


def test_get_sum_amount_missing_operation_amount_field(mock_currency_data):
    # Тест с операциями без поля operationAmount
    operations_missing_field = [
        {"description": "Payment"},
        {
            "operationAmount": {
                "amount": "100.00",
                "currency": {
                    "code": "RUB"
                }
            }
        }
    ]

    currency_path = os.path.join("..//exchangerates_data", "currency_USD_EUR.json")
    operations_path = os.path.join("..//data", "operations.json")

    with patch("builtins.open", side_effect=[
        mock_open(read_data=json.dumps(mock_currency_data)).return_value,
        mock_open(read_data=json.dumps(operations_missing_field)).return_value
    ]):
        result = get_sum_amount()

    # Должна учитываться только одна операция с полным набором данных
    assert result == 100.00
