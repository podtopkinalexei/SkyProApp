import re
from collections import Counter, defaultdict
from typing import Any, Dict, List, Optional

# from src.read_file import read_file


def find_common_words(transactions: List[Dict]) -> str:
    """Функция ищет в описании наиболее часто встречающиеся операции"""
    if not transactions:
        return "Нет данных для анализа"

    first_words = []
    valid_transactions = []

    for tx in transactions:
        if (
            isinstance(tx, dict)
            and "description" in tx
            and isinstance(tx["description"], str)
        ):
            valid_transactions.append(tx)
            # Удаляем знаки препинания и лишние пробелы
            clean_desc = re.sub(r"[^\w\s]", "", tx["description"].strip())
            desc_words = clean_desc.split()
            if desc_words:
                first_words.append(desc_words[0].lower())

    if not valid_transactions:
        return "В транзакциях отсутствуют описания"

    if first_words:
        word_counts = Counter(first_words)
        top_words = word_counts.most_common(5)

        print("\nПодсказка: Частые типы операций:")
        for word, count in top_words:
            print(f"- {word.capitalize()} ({count} операций)")

    return ""


def find_transactions_by_description(
    transactions: List[Dict], keyword: str = ""
) -> Optional[List[Dict]]:
    """Функция принимает список словарей с данными о банковских операциях и строку поиска и возвращает список словарей,
    у которых в описании есть данная строка."""

    if not transactions:
        print("Нет данных для анализа")
        return None

    # Проверяем, что все элементы - словари с описанием
    valid_transactions = []
    descriptions = []
    for tx in transactions:
        if (
            isinstance(tx, dict)
            and "description" in tx
            and isinstance(tx["description"], str)
        ):
            valid_transactions.append(tx)
            descriptions.append(tx["description"].lower())

    if not valid_transactions:
        print("В транзакциях отсутствуют описания")
        return None

    # Поиск транзакций по ключевому слову
    keyword_lower = keyword.lower()
    found = [
        tx for tx in valid_transactions if keyword_lower in tx["description"].lower()
    ]

    if not found:
        print(f"\nТранзакции с описанием, содержащим '{keyword}', не найдены")
        return None

    print(f"\nНайдено {len(found)} транзакций:")
    return found


def find_category_data(
    transactions: List[Dict[str, Any]], categories: List[str] = None
) -> Dict[str, int]:
    """Функция принимает список словарей с данными о банковских операциях и список категорий операций и возвращает словарь,
    в котором ключи — это названия категорий, а значения — это количество операций в каждой категории.
    """

    # Инициализируем словарь для статистики
    category_counts = defaultdict(int)

    # Компилируем регулярные выражения для каждой категории
    patterns = {
        category: re.compile(rf"\b{re.escape(category.lower())}\b", re.IGNORECASE)
        for category in categories
    }

    for transaction in transactions:
        if not isinstance(transaction, dict):
            continue

        description = transaction.get("description", "").lower()

        # Проверяем каждую категорию
        for category, pattern in patterns.items():
            if pattern.search(description):
                category_counts[category] += 1
                break

    return dict(category_counts)


# Для проверки
# keyword = "Открытие"
# list_categories = ("Открытие", "Перевод")
# path_to_file_csv = path_to_file_json = "../data/operations.json"
# data = read_file(path_to_file_csv)

# print(find_common_words(data))
# print(find_transactions_by_description(data, keyword))
# print(find_category_data(data, list_categories))
