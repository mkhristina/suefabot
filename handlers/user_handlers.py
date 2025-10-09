from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from keyboards.rsp_keyboard import game_kb, yes_no_kb
from keyboards.keyboards import select_game_kb
from keyboards.cube_keyboard import cube_kb, throw_or_back_kb
from lexicon.lexicon_ru import LEXICON_RU
from services.services import get_bot_choice, get_winner

router = Router()

# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'], reply_markup=select_game_kb)


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'], reply_markup=select_game_kb)


# Этот хэндлер срабатывает на согласие пользователя играть в игру камень - ножницы - бумага
@router.message(F.text == LEXICON_RU['rsp_game'])
async def process_yes_answer(message: Message):
    await message.answer(text=LEXICON_RU['yes'], reply_markup=game_kb)

# Этот хэндлер срабатывает на согласие пользователя играть в игру с кубиком
@router.message(F.text == LEXICON_RU['cube_game'])
async def process_yes_answer(message: Message):
    await message.answer(text=LEXICON_RU['yes_cube'], reply_markup=cube_kb)

# Этот хэндлер срабатывает на согласие пользователя играть в игру
@router.message(F.text == LEXICON_RU['yes_button'])
async def process_yes_answer(message: Message):
    await message.answer(text=LEXICON_RU['yes'], reply_markup=game_kb)


# Этот хэндлер срабатывает на отказ пользователя играть в игру
@router.message(F.text == LEXICON_RU['no_button'])
async def process_no_answer(message: Message):
    await message.answer(text=LEXICON_RU['no'])

# Этот хэндлер срабатывает при нажатии кнопки "Вернуться к выбору игры"
@router.message(F.text == LEXICON_RU['back_to_game_chooser'])
async def process_yes_answer(message: Message):
    await message.answer(text=LEXICON_RU['choose_game_submit'], reply_markup=select_game_kb)

# Этот хэндлер срабатывает при нажатии кнопки "Бросить кубик"
@router.message(F.text == LEXICON_RU['throw_cube'])
async def process_yes_answer(message: Message):
    await message.answer_dice(emoji='🎲', reply_markup=throw_or_back_kb)


# Этот хэндлер срабатывает на любую из игровых кнопок
@router.message(F.text.in_([LEXICON_RU['rock'],
                            LEXICON_RU['paper'],
                            LEXICON_RU['scissors']]))
async def process_game_button(message: Message):
    bot_choice = get_bot_choice()
    await message.answer(text=f'{LEXICON_RU["bot_choice"]} '
                              f'- {LEXICON_RU[bot_choice]}')
    winner = get_winner(message.text, bot_choice)
    await message.answer(text=LEXICON_RU[winner], reply_markup=yes_no_kb)
