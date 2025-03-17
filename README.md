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

Лицензия: Этот проект распространяется под лицензией MIT. Подробности см. в файле LICENSE.

Автор
Alexey Podtopkin


Ссылки:
[Python 3 Documentation](https://docs.python.org/3/)
[datetime Module](https://docs.python.org/3/library/datetime.html)
