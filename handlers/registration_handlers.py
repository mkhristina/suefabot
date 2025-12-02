from aiogram import F, Router, Dispatcher
from aiogram.types import Message
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from lexicon.lexicon_ru import LEXICON_RU
import csv
import re
from keyboards.keyboards import select_game_kb


router = Router()

dp = Dispatcher(storage=MemoryStorage())


# --- FSM для регистрации ---
class Registration(StatesGroup):
    FIO = State()
    Phone = State()


def is_registered(user_id):
    try:
        with open("users.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if str(user_id) == row[0]:
                    return True
    except FileNotFoundError:
        return False
    return False


# -------------------------------
# ВАЛИДАЦИЯ ДАННЫХ
# -------------------------------


def is_valid_fio(fio: str) -> bool:
    """
    ФИО: только буквы (рус/англ) + пробелы
    """
    return bool(re.fullmatch(r"[A-Za-zА-Яа-яЁё\s]+", fio))


def is_valid_phone(phone: str) -> bool:
    """
    Телефон: только цифры
    """
    return phone.isdigit()


# --- Регистрация пользователя ---
@router.message(F.text == "📝 Регистрация")
async def register(message: Message, state: FSMContext):
    if is_registered(message.from_user.id):
        await message.answer("Вы уже зарегистрированы!")
        return

    await message.answer("Введите ваше ФИО:")
    await state.set_state(Registration.FIO)


# --- Обработка ФИО ---
@router.message(Registration.FIO)
async def reg_fio(message: Message, state: FSMContext):

    # Проверка корректности ФИО
    if not is_valid_fio(message.text):
        await message.answer(
            "ФИО может содержать только буквы и пробелы.\nПопробуйте снова:"
        )
        return

    await state.update_data(fio=message.text)
    await message.answer("Введите ваш номер телефона:")
    await state.set_state(Registration.Phone)


# --- Обработка телефона ---
@router.message(Registration.Phone)
async def reg_phone(message: Message, state: FSMContext):

    # Проверка корректности номера телефона
    if not is_valid_phone(message.text):
        await message.answer(
            "Номер телефона может содержать только цифры.\nПопробуйте снова:"
        )
        return

    data = await state.get_data()
    user_id = message.from_user.id

    # Запись в CSV
    with open("users.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([user_id, data["fio"], message.text])

    await message.answer(text=LEXICON_RU["/start"], reply_markup=select_game_kb)
    await state.clear()
