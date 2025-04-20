import functools
import os
from datetime import datetime


def log(filename=None):
    """Декоратор 'log' автоматически записывает начало и конец выполнения функции,
    а также ее результаты или возникшие ошибки.
    Декоратор принимает необязательный аргумент 'filename':
    - Если 'filename' задан, логи записываются в указанный файл.
    - Если 'filename' не задан, логи выводятся в консоль."""

    def decorator_func(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            def make_dir(directory_name="logs"):
                """Функция создает директорию (по умолчанию 'logs') для размещения в ней файлов логирования"""
                try:
                    os.makedirs(directory_name, exist_ok=True)

                except PermissionError:
                    print(f"Permission denied: Unable to create '{directory_name}'.")
                except Exception as e:
                    print(f"An error occurred: {e}")
                return directory_name

            try:
                time_start = datetime.now()
                result = func(*args, **kwargs)
                time_end = datetime.now()
                delta_time = time_end - time_start
                message_output = (
                    f"{datetime.now().strftime('%d.%m.%y %H:%M:%S')}\n"
                    f"Function: '{func.__name__}'\n"
                    f"Time start: {time_start.strftime('%d.%m.%y %H:%M:%S')}\n"
                    f"Time end: {time_end.strftime('%d.%m.%y %H:%M:%S')}\n"
                    f"Time execution: {delta_time}\nresult: {result}\n"
                )
                if filename:
                    directory_name = make_dir()
                    filepath = os.path.join(directory_name, filename)
                    with open(filepath, "a", encoding="utf-8") as file:
                        file.write(message_output)
                else:
                    print(message_output)
                return result
            except Exception as e:
                message_error = (
                    f"{datetime.now().strftime('%d.%m.%y %H:%M:%S')}\n"
                    f"Function '{func.__name__}'"
                    f" raised an error: {type(e).__name__} - {e}. Args: {args}, kwargs: {kwargs}\n"
                )
                if filename:
                    directory_name = make_dir()
                    filepath = os.path.join(directory_name, filename)
                    with open(filepath, "a", encoding="utf-8") as file:
                        file.write(message_error)
                else:
                    print(message_error)
                raise

        return wrapper

    return decorator_func
