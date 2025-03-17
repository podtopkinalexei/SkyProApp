from datetime import datetime


def filter_by_state(user_data: list[dict], state: str = 'EXECUTED'):
    """Функция возвращает новый список словарей, содержащий только те словари, у которых ключ state
 соответствует указанному значению."""
    filtered_list_state = [list_state for list_state in user_data if list_state['state'] == state]
    return filtered_list_state


def sort_by_date(data_: list[dict], reverse=True):
    """Функция возвращает новый список, отсортированный по дате."""
    filtered_list_date = [sorted(data_, key=lambda x: datetime.fromisoformat(x['date']), reverse=reverse)]
    return filtered_list_date
