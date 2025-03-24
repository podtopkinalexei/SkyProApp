from datetime import datetime


def filter_by_state(user_data: list[dict], state: str = 'EXECUTED'):
    """Функция возвращает новый список словарей, содержащий только те словари, у которых ключ state
 соответствует указанному значению."""
    if not user_data:
        return "State not found"

    if not any(list_state.get('state') == state for list_state in user_data):
        return f"State not found"

    filtered_list_state = [list_state for list_state in user_data if list_state.get('state') == state]
    return filtered_list_state


def sort_by_date(data_: list[dict], reverse=True):
    """Функция возвращает новый список, отсортированный по дате."""
    filtered_list_date = [sorted(data_, key=lambda x: datetime.fromisoformat(x['date']), reverse=reverse)]
    return filtered_list_date


get_operation_list = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
                      {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
                      {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                      {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
                      {'id': 615064592, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]


print(filter_by_state(get_operation_list))
