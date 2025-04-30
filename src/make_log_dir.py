import logging
import os

default_directory_name = "../logs"
default_logs_path_name = "../logs/mkdir.log"

logger = logging.getLogger("mkdir")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(default_logs_path_name, mode="w")
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def make_dir(directory_name=default_directory_name):
    """Функция создает директорию (по умолчанию 'logs') для размещения в ней файлов логирования"""
    try:
        os.makedirs(directory_name, exist_ok=True)
        logger.debug("Directory was created successfully")

    except PermissionError as e:
        logger.error(f"Error: {e}")
        print(f"Permission denied: Unable to create '{directory_name}'.")

    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"An error occurred: {e}")

    return None
