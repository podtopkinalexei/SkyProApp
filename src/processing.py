from datetime import datetime
from typing import Dict, List, Union


def filter_by_state(
    user_data: List[Dict[str, str]], state: str = "EXECUTED"
) -> Union[List[Dict[str, str]], str]:
    """Функция возвращает новый список словарей, содержащий только те словари, у которых ключ state
    соответствует указанному значению."""
    if not user_data:
        return f"State not found"

    if not any(list_state.get("state") == state for list_state in user_data):
        return f"State not found"

    filtered_list_state = [
        list_state for list_state in user_data if list_state.get("state") == state
    ]
    return filtered_list_state


def sort_by_date(
    data_: List[Dict[str, str]], reverse: bool = True
) -> str | list[list[dict[str, str]]]:
    """Функция возвращает новый список, отсортированный по дате."""
    if not data_:
        return f"There is no data available for filtering"

    filtered_list_date = [
        sorted(data_, key=lambda x: datetime.fromisoformat(x["date"]), reverse=reverse)
    ]
    return filtered_list_date
