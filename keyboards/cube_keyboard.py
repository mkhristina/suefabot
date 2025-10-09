from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU

throw_cube_button = KeyboardButton(text=LEXICON_RU['throw_cube'])

# Создаем клавиатуру с выбором игры
cube_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[throw_cube_button]],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Создаем кнопки с предложением еще раз кинуть или вернуться к выбору игры
button_back_to_game_chooser = KeyboardButton(text=LEXICON_RU['back_to_game_chooser'])

# Инициализируем билдер для клавиатуры с кнопками "Бросить кубик" и "Вернуться к выбору игры"
yes_no_kb_builder = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер с аргументом width=2
yes_no_kb_builder.row(throw_cube_button, button_back_to_game_chooser, width=2)

# Создаем клавиатуру с кнопками "Бросить кубик" и "Вернуться к выбору игры"
throw_or_back_kb: ReplyKeyboardMarkup = yes_no_kb_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
)