import os


def make_dir(directory_name="logs"):
    """Функция создает директорию (по умолчанию 'logs') для размещения в ней файлов логирования"""
    try:
        os.makedirs(directory_name, exist_ok=True)

    except PermissionError:
        print(f"Permission denied: Unable to create '{directory_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return directory_name
