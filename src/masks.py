import logging

# from src.make_log_dir import make_dir
#
# make_dir()

default_logs_path_name = "../logs/masks.log"

logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(default_logs_path_name, mode="w")
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Функция принимает на вход номер карты и возвращает ее маску формате XXXX XX** **** XXXX"""
    if len(card_number) != 16 or not card_number.isdigit():
        logger.error(f"Failure. Invalid card number: {card_number}")
        return "Invalid card number"
    else:
        logger.info("Success")
        return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(bank_account: str) -> str:
    """Функция принимает на вход номер счета и возвращает его маску формате **XXXX"""
    if len(bank_account) != 20 or not bank_account.isdigit():
        logger.error(f"Failure. Invalid bank account: {bank_account}")
        return "Invalid bank account"
    else:
        logger.info("Success")
        return f"**{bank_account[-4:]}"
