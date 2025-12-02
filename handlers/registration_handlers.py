from aiogram import F, Router, Dispatcher
from aiogram.types import Message
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from lexicon.lexicon_ru import LEXICON_RU
import csv
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
                if str(user_id) == row[0]:  # user_id в первой колонке
                    return True
    except FileNotFoundError:
        return False
    return False


# --- Регистрация пользователя ---
@router.message(F.text == "📝 Регистрация")
async def register(message: Message, state: FSMContext):
    if is_registered(message.from_user.id):
        await message.answer("Вы уже зарегистрированы!")
        return
    await message.answer("Введите ваше ФИО:")
    await state.set_state(Registration.FIO)


@router.message(Registration.FIO)
async def reg_fio(message: Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await message.answer("Введите ваш номер телефона:")
    await state.set_state(Registration.Phone)


@router.message(Registration.Phone)
async def reg_phone(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id

    # Запись в CSV
    with open("users.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([user_id, data["fio"], message.text])

    await message.answer(text=LEXICON_RU["/start"], reply_markup=select_game_kb)
    await state.clear()
