from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon_ru import LEXICON_RU

router = Router()


# Хэндлер для сообщений, которые не попали в другие хэндлеры
@router.message()
async def send_answer(message: Message):
    await message.answer_animation("https://media1.tenor.com/m/5_k7yVXmLlsAAAAC/idk-shrug.gif")
    await message.answer(text=LEXICON_RU["other_answer"])
