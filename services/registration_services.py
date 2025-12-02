import re


def is_valid_name(name: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-zА-Яа-яЁё\s]+", name))


def is_valid_phone(phone: str) -> bool:
    return phone.isdigit()
