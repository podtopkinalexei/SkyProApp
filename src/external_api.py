import json
import os

import requests
from dotenv import load_dotenv

load_dotenv(override=True)

API_KEY = os.getenv('API_KEY')


def get_currency_rate() -> int:
    """Функция плучает по API курс валют"""
    url = "https://api.apilayer.com/exchangerates_data/latest?symbols=USD%2CEUR&base=RUB"

    payload = {}
    headers = {
        "apikey": API_KEY
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    status_code = response.status_code
    data = response.json()

    def make_dir(directory_name: str = "..\\exchangerates_data"):
        """Функция создает директорию (по умолчанию 'exchangerates_data') для размещения в ней файлов логирования"""
        try:
            os.makedirs(directory_name, exist_ok=True)

        except PermissionError:
            print(f"Permission denied: Unable to create '{directory_name}'.")
        except Exception as e:
            print(f"An error occurred: {e}")
        return directory_name

    directory_name = make_dir()
    filename = "currency_USD_EUR.json"
    filepath = os.path.join(directory_name, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return status_code
