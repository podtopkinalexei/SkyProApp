from src.processing import filter_by_state, sort_by_date
from tests.conftest import get_operation_list


def test_filter_by_state(get_operation_list):
    assert filter_by_state(get_operation_list, "EXECUTED") == [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]

    assert filter_by_state(get_operation_list, "CANCELED") == [
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 615064592, "state": "CANCELED", "date": "2018-10-14T08:21:30.419128"},
    ]
    assert filter_by_state(get_operation_list, "ERROR") == "State not found"

    assert filter_by_state(get_operation_list, "") == "State not found"


def test_sort_by_date(get_operation_list):
    assert sort_by_date(get_operation_list) == [
        [
            {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {
                "id": 615064591,
                "state": "CANCELED",
                "date": "2018-10-14T08:21:33.419441",
            },
            {
                "id": 615064592,
                "state": "CANCELED",
                "date": "2018-10-14T08:21:30.419128",
            },
            {
                "id": 594226727,
                "state": "CANCELED",
                "date": "2018-09-12T21:27:25.241689",
            },
            {
                "id": 939719570,
                "state": "EXECUTED",
                "date": "2018-06-30T02:08:58.425572",
            },
        ]
    ]

    assert sort_by_date(get_operation_list, False) == [
        [
            {
                "id": 939719570,
                "state": "EXECUTED",
                "date": "2018-06-30T02:08:58.425572",
            },
            {
                "id": 594226727,
                "state": "CANCELED",
                "date": "2018-09-12T21:27:25.241689",
            },
            {
                "id": 615064592,
                "state": "CANCELED",
                "date": "2018-10-14T08:21:30.419128",
            },
            {
                "id": 615064591,
                "state": "CANCELED",
                "date": "2018-10-14T08:21:33.419441",
            },
            {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        ]
    ]

    assert sort_by_date("") == "There is no data available for filtering"
