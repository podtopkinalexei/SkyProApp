from unittest.mock import patch

from src.external_api import get_currency_rate


@patch("requests.get")
def test_get_currency_rate(mock_get):
    mock_get.return_value.json.return_value = 200
    assert get_currency_rate() == 200
