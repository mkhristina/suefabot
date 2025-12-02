from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU

# Создаем кнопки с предложением еще раз кинуть или вернуться к выбору игры
button_back_to_game_chooser = KeyboardButton(text=LEXICON_RU['back_to_game_chooser'])

# Инициализируем билдер для клавиатуры с кнопками "Бросить кубик" и "Вернуться к выбору игры"
back_to_menu = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер
back_to_menu.row(button_back_to_game_chooser)

# Создаем клавиатуру с кнопками "Бросить кубик" и "Вернуться к выбору игры"
back_to_menu_kb: ReplyKeyboardMarkup = back_to_menu.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
)