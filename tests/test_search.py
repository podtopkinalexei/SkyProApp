from unittest.mock import patch

from src.search import (
    find_category_data,
    find_common_words,
    find_transactions_by_description,
)

# Тестовые данные
sample_transactions = [
    {"description": "Перевод организации", "amount": "1000"},
    {"description": "Покупка в магазине", "amount": "500"},
    {"description": "Перевод с карты на карту", "amount": "2000"},
    {"description": "Оплата услуг", "amount": "1500"},
    {"description": "Перевод организации", "amount": "3000"},
    {"description": "Покупка билетов", "amount": "700"},
]


def test_empty_transactions():
    """Тест пустого списка транзакций"""
    result = find_common_words([])
    assert result == "Нет данных для анализа"


def test_no_descriptions():
    """Тест транзакций без описаний"""
    transactions = [{"amount": "100"}, {}]
    result = find_common_words(transactions)
    assert result == "В транзакциях отсутствуют описания"


def test_valid_transactions():
    """Тест корректных данных"""
    with patch("builtins.print") as mock_print:
        result = find_common_words(sample_transactions)
        assert result == ""

        # Проверяем вывод
        output = "\n".join([call[0][0] for call in mock_print.call_args_list])
        assert "Подсказка: Частые типы операций:" in output
        assert "- Перевод (3 операций)" in output
        assert "- Покупка (2 операций)" in output
        assert "- Оплата (1 операций)" in output


def test_case_insensitivity():
    """Тест регистронезависимости"""
    transactions = [
        {"description": "перевод организации"},
        {"description": "Перевод с карты"},
        {"description": "ПЕРЕВОД средств"},
    ]
    with patch("builtins.print") as mock_print:
        find_common_words(transactions)
        output = "\n".join([call[0][0] for call in mock_print.call_args_list])
        assert "- Перевод (3 операций)" in output


def test_special_characters():
    """Тест специальных символов в описаниях"""
    transactions = [
        {"description": "  Перевод! организации  "},
        {"description": "Покупка: в магазине"},
    ]
    with patch("builtins.print") as mock_print:
        find_common_words(transactions)
        output = "\n".join([call[0][0] for call in mock_print.call_args_list])
        assert "- Перевод (1 операций)" in output
        assert "- Покупка (1 операций)" in output


def test_short_descriptions():
    """Тест коротких описаний"""
    transactions = [
        {"description": "Перевод"},
        {"description": "Покупка"},
        {"description": "Перевод"},
    ]
    with patch("builtins.print") as mock_print:
        find_common_words(transactions)
        output = "\n".join([call[0][0] for call in mock_print.call_args_list])
        assert "- Перевод (2 операций)" in output
        assert "- Покупка (1 операций)" in output


def test_empty_transactions():
    """Тест пустого списка транзакций"""
    with patch("builtins.print") as mock_print:
        result = find_transactions_by_description([])
        assert result is None
        mock_print.assert_called_with("Нет данных для анализа")


def test_no_descriptions():
    """Тест транзакций без описаний"""
    transactions = [{"amount": "100"}, {}]
    with patch("builtins.print") as mock_print:
        result = find_transactions_by_description(transactions)
        assert result is None
        mock_print.assert_called_with("В транзакциях отсутствуют описания")


def test_keyword_found():
    """Тест успешного поиска по ключевому слову"""
    with patch("builtins.print") as mock_print:
        result = find_transactions_by_description(sample_transactions, "перевод")
        assert len(result) == 3
        assert all("перевод" in tx["description"].lower() for tx in result)
        mock_print.assert_called_with("\nНайдено 3 транзакций:")


def test_keyword_not_found():
    """Тест случая когда ключевое слово не найдено"""
    with patch("builtins.print") as mock_print:
        result = find_transactions_by_description(sample_transactions, "кредит")
        assert result is None
        mock_print.assert_called_with(
            "\nТранзакции с описанием, содержащим 'кредит', не найдены"
        )


def test_case_insensitivity():
    """Тест регистронезависимости поиска"""
    with patch("builtins.print"):
        result = find_transactions_by_description(sample_transactions, "ПЕРЕВОД")
        assert len(result) == 3
        result = find_transactions_by_description(sample_transactions, "покупка")
        assert len(result) == 2


def test_empty_keyword():
    """Тест пустой строки поиска"""
    with patch("builtins.print"):
        result = find_transactions_by_description(sample_transactions)
        assert len(result) == len(sample_transactions)


def test_special_characters():
    """Тест специальных символов в описаниях"""
    transactions = [
        {"description": "Перевод! организации"},
        {"description": "Покупка: в магазине"},
    ]
    with patch("builtins.print"):
        result = find_transactions_by_description(transactions, "перевод")
        assert len(result) == 1
        result = find_transactions_by_description(transactions, "покупка")
        assert len(result) == 1


def test_empty_transactions():
    """Тест пустого списка транзакций"""
    result = find_category_data([], ["перевод", "покупка"])
    assert result == {}


def test_empty_categories():
    """Тест пустого списка категорий"""
    result = find_category_data(sample_transactions, [])
    assert result == {}


def test_no_matching_categories():
    """Тест когда нет совпадений по категориям"""
    result = find_category_data(sample_transactions, ["кредит", "депозит"])
    assert result == {}


def test_single_category():
    """Тест одной категории"""
    result = find_category_data(sample_transactions, ["перевод"])
    assert result == {"перевод": 3}


def test_multiple_categories():
    """Тест нескольких категорий"""
    result = find_category_data(sample_transactions, ["перевод", "покупка", "оплата"])
    assert result == {"оплата": 1, "перевод": 3, "покупка": 2}


def test_case_insensitivity():
    """Тест регистронезависимости"""
    result = find_category_data([{"description": "ПЕРЕВОД Организации"}], ["Перевод"])
    assert result == {"Перевод": 1}


def test_word_boundaries():
    """Тест поиска по целым словам"""
    transactions = [{"description": "Денежный перевод"}]
    result = find_category_data(transactions, ["перевод"])
    assert result == {"перевод": 1}


def test_special_characters():
    """Тест специальных символов в описаниях"""
    transactions = [
        {"description": "Перевод! организации"},
        {"description": "Покупка: в магазине"},
    ]
    result = find_category_data(transactions, ["перевод", "покупка"])
    assert result == {"перевод": 1, "покупка": 1}
