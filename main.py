from typing import Any, Dict, List, Optional

from src.generators import filter_by_currency
from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.read_file import read_file
from src.search import find_common_words
from src.widget import get_date


def main() -> str:
    # 1. Функция загрузки данных
    def get_choice_data() -> Optional[List[Dict[str, Any]]]:
        """Загружает данные из выбранного файла"""
        print(
            "Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями."
        )
        print(
            """Выберите источник данных:
              1. JSON-файл
              2. CSV-файл
              3. Excel-файл
              q - Выход"""
        )

        file_paths = {
            1: "data/operations.json",
            2: "data/transactions.csv",
            3: "data/transactions_excel.xlsx",
        }

        try:
            while True:
                choice = input("\nВведите номер (1-3) или 'q': ").strip().lower()

                if choice == "q":
                    print("Выход из программы")
                    return None

                if choice.isdigit() and int(choice) in file_paths:
                    data = read_file(file_paths[int(choice)])
                    if data:
                        print(
                            f"\nДанные успешно загружены из {['JSON', 'CSV', 'Excel'][int(choice) - 1]}-файла"
                        )
                        return data
                    print("Ошибка: Не удалось загрузить данные")
                else:
                    print("Ошибка: Введите число от 1 до 3")

        except KeyboardInterrupt:
            print("\nЗагрузка данных прервана")
            return None

    # Загружаем данные
    if (initial_data := get_choice_data()) is None:
        return

    # 2. Функция фильтрации по статусу
    def filter_by_status(data: List[Dict[str, Any]]) -> Optional[List[Dict[str, Any]]]:
        """Фильтрует операции по статусу"""
        statuses = {
            "1": ("EXECUTED", "Исполненные"),
            "2": ("CANCELED", "Отмененные"),
            "3": ("PENDING", "Ожидающие"),
        }

        print("\nФильтр по статусу операции:")
        print("1. Исполненные (EXECUTED)")
        print("2. Отмененные (CANCELED)")
        print("3. Ожидающие (PENDING)")
        print("0. Пропустить фильтр")

        while True:
            choice = input("Выберите статус (1-3) или 0: ").strip()

            if choice == "0":
                print("Фильтрация по статусу пропущена")
                return None

            if choice in statuses:
                code, name = statuses[choice]
                result = filter_by_state(data, code)
                print(f"\nПрименен фильтр: {name} операции")
                return result

            print("Ошибка: Введите число от 0 до 3")

    current_data = filter_by_status(initial_data) or initial_data

    # 3. Функция сортировки по дате
    def sort_transactions(data: List[Dict[str, Any]]) -> Optional[List[Dict[str, Any]]]:
        """Сортирует операции по дате"""
        print("\nСортировка по дате:")
        print("1. Сначала новые")
        print("2. Сначала старые")
        print("0. Не сортировать")

        while True:
            choice = input("Выберите вариант (1-2) или 0: ").strip()

            if choice == "0":
                print("Сортировка пропущена")
                return None

            if choice == "1":
                return sort_by_date(data, reverse=True)
            if choice == "2":
                return sort_by_date(data, reverse=False)

            print("Ошибка: Введите 0, 1 или 2")

    current_data = sort_transactions(current_data) or current_data

    # 4. Функция фильтрации по валюте
    def filter_by_currency_type(
        data: List[Dict[str, Any]],
    ) -> Optional[List[Dict[str, Any]]]:
        """Фильтрует операции по валюте"""
        print("\nФильтр по валюте:")
        print("1. Только рублевые операции")
        print("2. Только долларовые операции")
        print("0. Пропустить фильтр")

        while True:
            choice = input("Выберите вариант (1-2) или 0: ").strip()

            if choice == "0":
                print("Фильтрация по валюте пропущена")
                return None

            currencies = {"1": "RUB", "2": "USD"}
            if choice in currencies:
                result = list(filter_by_currency(data, currencies[choice]))
                if result:
                    print(f"\nНайдено {len(result)} операций в {currencies[choice]}")
                    return result
                print(f"Операций в {currencies[choice]} не найдено")
                return None

            print("Ошибка: Введите 0, 1 или 2")

    current_data = filter_by_currency_type(current_data) or current_data

    # 5. Функция поиска по ключевому слову
    def search_by_keyword(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Поиск операций по ключевому слову"""
        print("\nПоиск по ключевому слову в описании:")

        # Показываем подсказки
        if keywords := find_common_words(data):
            print(f"Частые слова: {', '.join(keywords[:5])}...")

        while True:
            keyword = (
                input("Введите слово для поиска (или Enter чтобы пропустить): ")
                .strip()
                .lower()
            )

            if not keyword:
                print("Поиск по ключевому слову пропущен")
                return data

            result = [
                tx
                for tx in data
                if isinstance(tx.get("description"), str)
                and keyword in tx["description"].lower()
            ]

            if result:
                print(f"Найдено {len(result)} операций")
                return result

            print("Совпадений не найдено. Попробуйте другое слово")

    final_data = search_by_keyword(current_data)

    def print_transactions(transactions: List[Dict[str, Any]]) -> None:
        """Выводит транзакции в требуемом формате или сообщение об отсутствии данных"""
        if not transactions:
            print(
                "\nПрограмма: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации"
            )
            return

        print(f"\nВсего банковских операций в выборке: {len(transactions)}\n")

        for tx in transactions:
            try:
                # Форматируем дату
                date = get_date(tx.get("date", ""))

                # Получаем описание
                description = tx.get("description", "Без описания")

                # Обрабатываем сумму и валюту
                amount_info = tx.get("operationAmount", {})
                amount = amount_info.get("amount", "0")
                currency_info = amount_info.get("currency", {})
                currency_code = currency_info.get("code", "")
                currency_name = currency_info.get("name", "")

                # Используем название валюты, если код отсутствует
                currency_display = currency_code if currency_code else currency_name

                # Маскируем номера карт/счетов
                from_account = ""
                if "from" in tx and isinstance(tx["from"], str):
                    if "счет" in tx["from"].lower():
                        acc_num = "".join(c for c in tx["from"] if c.isdigit())
                        from_account = f"Счет {get_mask_account(acc_num)}"
                    else:
                        card_num = "".join(c for c in tx["from"] if c.isdigit())
                        from_account = get_mask_card_number(card_num)

                to_account = ""
                if "to" in tx and isinstance(tx["to"], str):
                    if "счет" in tx["to"].lower():
                        acc_num = "".join(c for c in tx["to"] if c.isdigit())
                        to_account = f"Счет {get_mask_account(acc_num)}"
                    else:
                        card_num = "".join(c for c in tx["to"] if c.isdigit())
                        to_account = get_mask_card_number(card_num)

                # Формируем строку перевода
                transfer_info = ""
                if from_account and to_account:
                    transfer_info = f"{from_account} -> {to_account}"
                elif from_account:
                    transfer_info = f"{from_account} -> "
                elif to_account:
                    transfer_info = f"-> {to_account}"

                # Выводим информацию о транзакции
                print(f"{date} {description}")
                if transfer_info:
                    print(transfer_info)
                print(f"Сумма: {amount} {currency_display}\n")

            except Exception as e:
                print(
                    f"Ошибка обработки транзакции: {tx.get('id', 'без ID')} - {str(e)}"
                )
                continue

    if final_data:
        print_transactions(final_data)
    else:
        print("Нет данных для отображения")


if __name__ == "__main__":
    main()
