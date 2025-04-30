import json
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd

from src.read_file import read_file


@patch('pandas.read_csv')
@patch('builtins.open', new_callable=mock_open)
@patch('csv.Sniffer')
def test_read_csv_file(mock_sniffer, mock_open, mock_read_csv):
    mock_sniffer_instance = MagicMock()
    mock_sniffer_instance.sniff.return_value.delimiter = ';'
    mock_sniffer.return_value = mock_sniffer_instance

    test_df = pd.DataFrame({
        'id': [650703],
        'status': ['EXECUTED'],
        'date': ['2023-09-05T11:30:32Z']
    })
    mock_read_csv.return_value = test_df

    result = read_file('test.csv')

    assert isinstance(result, str)
    json_data = json.loads(result)
    assert len(json_data) == 1
    assert json_data[0]['id'] == 650703

    mock_open.assert_called_once()
    mock_sniffer.assert_called_once()
    mock_read_csv.assert_called_once()


@patch('pandas.read_excel')
def test_read_excel_file(mock_read_excel):
    test_df = pd.DataFrame({
        'id': [650703],
        'status': ['EXECUTED'],
        'date': ['2023-09-05T11:30:32Z']
    })
    mock_read_excel.return_value = test_df
    result = read_file('test.xlsx')

    assert isinstance(result, str)
    json_data = json.loads(result)
    assert len(json_data) == 1
    assert json_data[0]['id'] == 650703

    mock_read_excel.assert_called_once_with('test.xlsx')


@patch('builtins.open', new_callable=mock_open, read_data=json.dumps([{'id': 650703, 'status': 'EXECUTED'}]))
@patch('json.load')
def test_read_json_file(mock_json_load, mock_file):
    mock_json_load.return_value = [{'id': 650703, 'status': 'EXECUTED'}]
    result = read_file('test.json')

    assert isinstance(result, str)
    json_data = json.loads(result)
    assert len(json_data) == 1
    assert json_data[0]['id'] == 650703

    mock_file.assert_called_once_with('test.json', 'r', encoding='utf-8')
    mock_json_load.assert_called_once()


@patch('pandas.read_csv')
def test_empty_file(mock_read_csv):
    mock_read_csv.return_value = pd.DataFrame()
    result = read_file('empty.csv')

    assert result == "Ошибка при чтении CSV: [Errno 2] No such file or directory: 'empty.csv'"


@patch('builtins.open', side_effect=FileNotFoundError)
def test_nonexistent_file(mock_open):
    result = read_file('nonexistent.csv')

    assert "Ошибка при чтении CSV" in result


def test_unsupported_extension():
    result = read_file('test.txt')

    assert result == "Укажите файл с расширением .csv, .xlsx/.xls или .json"


@patch('builtins.open', new_callable=mock_open, read_data='{invalid json}')
@patch('json.load', side_effect=json.JSONDecodeError('Expecting value', 'test.json', 1))
def test_invalid_json(mock_json_load, mock_file):
    result = read_file('invalid.json')

    assert "Ошибка при чтении .json: Expecting value: line 1 column 2 (char 1)" in result


@patch('pandas.DataFrame.to_json')
@patch('pandas.read_csv')
def test_json_conversion_error(mock_read_csv, mock_to_json):
    test_df = pd.DataFrame({'id': [650703]})
    mock_read_csv.return_value = test_df
    mock_to_json.side_effect = Exception('Conversion error')

    result = read_file('test.csv')

    assert "Ошибка при чтении CSV: [Errno 2] No such file or directory: 'test.csv'" in result
