# Учебный Проект на Python3.
Ппроект предоставляет две функции для работы со списком словарей, содержащих данные о транзакциях или других операциях.
Основная задача — фильтрация по состоянию (state) и сортировка по дате (date).
## Установка
Установка
Для использования проекта необходимо установить `Python 3.7` или выше.
Дополнительные зависимости не требуются.

## Использование
### Функции
1. Фильтр списка словарей по значению ключа state.
```
filter_by_state(user_data: list[dict], state: str = 'EXECUTED') -> list[dict]
```
Параметры:
`user_data:` Список словарей, где каждый словарь содержит ключ state.

`state:` Значение для фильтрации (по умолчанию 'EXECUTED').

Возвращает: Новый список словарей, где значение ключа state соответствует указанному.

Пример:
```
data = [
    {"state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"},
    {"state": "PENDING", "date": "2024-03-10T12:00:00.000000"},
      ]
filtered_data = filter_by_state(data)
print(filtered_data)
# Вывод: [{"state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"}]
```
2. Сортировка списка словарей по ключу date.
```
sort_by_date(data_: list[dict], reverse=True) -> list[dict]
```
Параметры:

`data_:` Список словарей, где каждый словарь содержит ключ date в формате ISO (YYYY-MM-DDTHH:MM:SS).

`reverse:` Если True, сортировка выполняется по убыванию (по умолчанию True).

Возвращает: Новый список словарей, отсортированный по дате.

Пример:

```
data = [
    {"state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"},
    {"state": "EXECUTED", "date": "2024-03-10T12:00:00.000000"},
      ]

sorted_data = sort_by_date(data)
print(sorted_data)
# Вывод: [
#     {"state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"},
#     {"state": "EXECUTED", "date": "2024-03-10T12:00:00.000000"},
#       ]
```
Пример использования:
```
from datetime import datetime

# Пример данных
transactions = [
    {"state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"},
    {"state": "PENDING", "date": "2024-03-10T12:00:00.000000"},
    {"state": "EXECUTED", "date": "2024-03-09T08:15:45.123456"},
]

# Фильтрация по состоянию
filtered_transactions = filter_by_state(transactions)
print("Фильтрованные данные:", filtered_transactions)

# Сортировка по дате
sorted_transactions = sort_by_date(filtered_transactions)
print("Отсортированные данные:", sorted_transactions)
```

3. Фильтрует транзакции по заданной валюте и возвращает итератор.

```
filter_by_currency(transactions: list[dict], select_currency: str = "USD") -> Iterator[dict]`
```

Параметры:
`transactions` - список словарей с транзакциями
`select_currency` - код валюты для фильтрации (по умолчанию "USD")

Возвращает:  
Итератор, который поочередно возвращает транзакции в указанной валюте.

Пример использования:

```
for transaction in filter_by_currency(transactions, "EUR"):
    print(transaction)
```    

4. Функции для работы с банковскими транзакциями и картами

```
filter_by_currency(transactions: list[dict], select_currency: str = "USD") -> Iterator[dict]
```

Фильтрует транзакции по заданной валюте и возвращает итератор.
Параметры:

`transactions` — список транзакций (каждая транзакция — словарь).

`select_currency` — код валюты для фильтрации (по умолчанию "USD").

Возвращает:
Итератор, который поочередно возвращает транзакции с указанной валютой.

Пример использования:

```
for transaction in filter_by_currency(transactions, "EUR"):
    print(transaction)
```

5. Генератор номера банковских карт в заданном диапазоне.

```
card_number_generator(start: int, end: int) -> Iterator[str]
```

Параметры:

`start` — начальный номер карты (целое число, от 0 до 9999999999999999).

`end` — конечный номер карты (целое число, от 0 до 9999999999999999).

Возвращает:
Итератор, который поочередно возвращает номера карт в формате XXXX XXXX XXXX XXXX.

Пример использования:

```
for card_number in card_number_generator(1, 5):
    print(card_number)
```

# Вывод:

# 0000 0000 0000 0001

# 0000 0000 0000 0002

# ...

# 0000 0000 0000 0005

Примечание:
Если диапазон некорректен (например, start > end или число вне допустимых границ), функция выведет "Incorrect range".

Лицензия: Этот проект распространяется под лицензией MIT. Подробности см. в файле LICENSE.

Автор
Alexey Podtopkin


Ссылки:
[Python 3 Documentation](https://docs.python.org/3/)
[datetime Module](https://docs.python.org/3/library/datetime.html)
