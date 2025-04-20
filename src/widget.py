from datetime import datetime


def mask_account_card(card_number: str) -> list[Any]:
    """Функция маскировки номера"""
    type_data = "счет"
    type_data_alt = "счёт"

    text_data = " ".join([data_ for data_ in card_number.split() if data_.isalpha()])
    number_ = "".join([data_ for data_ in card_number.split() if not data_.isalpha()])

    if (type_data in text_data.lower() or type_data_alt in text_data.lower()) and len(number_) == 20:
        number_card = f"**{number_[-4:]}"
        return f"{text_data} {number_card}"

    elif len(number_) != 16 or not number_.isdigit() or len(text_data) == 0:
        return "Invalid card or account number"

    else:
        number_card = f"{"".join(number_)[:4]} {"".join(number_)[4:6]}** **** {"".join(number_)[-4:]}"
        return f"{text_data} {number_card}"


def get_date(incoming_date):
    """Функция конвертирования даты из формата iso в формат ДД.ММ.ГГ"""
    if incoming_date != "":
        return datetime.fromisoformat(incoming_date).strftime("%d.%m.%Y")
    else:
        return "Invalid date"
