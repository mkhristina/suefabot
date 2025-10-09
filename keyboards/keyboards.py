from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from lexicon.lexicon_ru import LEXICON_RU

# ------- Создаем клавиатуру для выбора игры через ReplyKeyboardMarkup -------
button_rsp = KeyboardButton(text=LEXICON_RU['rsp_game'])
button_cube = KeyboardButton(text=LEXICON_RU['cube_game'])

# Создаем клавиатуру с выбором игры
select_game_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[button_rsp, button_cube]],
    resize_keyboard=True,
    one_time_keyboard=True
)
