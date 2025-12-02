import random

from lexicon.lexicon_ru import LEXICON_RU
from keyboards.keyboards import select_game_kb_admin, select_game_kb


# Функция, возвращающая случайный выбор бота в игре
def get_bot_choice() -> str:
    return random.choice(["rock_button", "paper", "scissors"])


# Функция, возвращающая ключ из словаря, по которому
# хранится значение, передаваемое как аргумент - выбор пользователя
def _normalize_user_answer(user_answer: str) -> str:
    for key in LEXICON_RU:
        if LEXICON_RU[key] == user_answer:
            break
    return key


# Функция, определяющая победителя
def get_winner(user_choice: str, bot_choice: str) -> str:
    user_choice = _normalize_user_answer(user_choice)
    rules = {"rock_button": "scissors", "scissors": "paper", "paper": "rock_button"}
    if user_choice == bot_choice:
        return "nobody_won"
    elif rules[user_choice] == bot_choice:
        return "user_won"
    return "bot_won"


ADMIN_ID = 2059351969


def is_admin(id):
    return id == ADMIN_ID


def get_keyboard_for_select_game(user_id):
    if is_admin(user_id):
        return select_game_kb_admin
    else:
        return select_game_kb
