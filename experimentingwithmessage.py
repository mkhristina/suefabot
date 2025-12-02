from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
    Message,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import CommandStart
from aiogram.exceptions import TelegramBadRequest

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
BOT_TOKEN = "8315368143:AAHTCOIzx5BQI9o904Q98pAvJaadJzddnv4"

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


LEXICON: dict[str, str] = {
    "audio": "🎶 Аудио",
    "text": "📃 Текст",
    "photo": "🖼 Фото",
    "video": "🎬 Видео",
    "document": "📑 Документ",
    "voice": "📢 Голосовое сообщение",
    "text_1": "Это обыкновенное текстовое сообщение, его можно легко "
    "отредактировать другим текстовым сообщением, но нельзя отредактировать "
    "сообщением с медиа.",
    "text_2": "Это тоже обыкновенное текстовое сообщение, которое можно "
    "заменить на другое текстовое сообщение через редактирование.",
    "photo_id1": "AgACAgIAAxkBAAID32kSM_3fXLiCjuUWLahyERF27YAnAAIaEWsbJW-QSNh1sFI_95-wAQADAgADeQADNgQ",
    "photo_id2": "BQACAgIAAxkBAAID-2kSNs8Oj1a0_039Qqoy7uGWG3Z5AALZkwACJW-QSKroXY0okKqYNgQ",
    "voice_id1": "AwACAgIAAxkBAAID_GkSNy-sbOwdH09KqlZtqSObHKvhAALekwACJW-QSAiHSMZl958PNgQ",
    "voice_id2": "AwACAgIAAxkBAAID_WkSNzK6BQWavpC93sdM_IsV0vo9AALfkwACJW-QSDd6LpV7QznTNgQ",
    "audio_id1": "CQACAgIAAxkBAAID92kSNia-x1KP6DrSr_8svhSTDkdDAALGkwACJW-QSALLfM3Qi68VNgQ",
    "audio_id2": "CQACAgIAAxkBAAID-WkSNsA6K-Jd9tKt6yQbIvZCuoi2AALXkwACJW-QSBd4k94uoGOANgQ",
    "document_id1": "BQACAgIAAxkBAAID9WkSNiGeAAH4UBf7eo71E4lmfBujuQACxJMAAiVvkEj6scgopqz3izYE",
    "document_id2": "BQACAgIAAxkBAAID9mkSNiPMJExUTVVv4wkkpav1G38MAALFkwACJW-QSN4ddOkKoW1_NgQ",
    "video_id1": "DQACAgIAAxkBAAID8WkSNfQDrKHFVEveTGejf9Ak-x6JAALAkwACJW-QSJZF0XN5qg_DNgQ",
    "video_id2": "DQACAgIAAxkBAAID9GkSNhbYbT0HqhLwExuVFR6412E7AALDkwACJW-QSNKtsOWhOLe9NgQ",
}


# Функция для генерации клавиатур с инлайн-кнопками
def get_markup(width: int, *args, **kwargs) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(
                InlineKeyboardButton(
                    text=LEXICON[button] if button in LEXICON else button,
                    callback_data=button,
                )
            )
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(text=text, callback_data=button))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(CommandStart())
async def process_start_command(message: Message):
    markup = get_markup(2, "voice")
    await message.answer_audio(
        audio=LEXICON["voice_id1"],
        caption="Это голосовое сообщение 1",
        reply_markup=markup,
    )


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
@dp.callback_query(F.data.in_(["text", "audio", "video", "document", "photo", "voice"]))
async def process_button_press(callback: CallbackQuery, bot: Bot):
    markup = get_markup(2, "voice")
    try:
        await bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=InputMediaAudio(
                media=LEXICON["voice_id2"], caption="Это голосове сообщение 2"
            ),
            reply_markup=markup,
        )
    except TelegramBadRequest:
        await bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=InputMediaAudio(
                media=LEXICON["voice_id1"], caption="Это голосове сообщение 1"
            ),
            reply_markup=markup,
        )


# Этот хэндлер будет срабатывать на все остальные сообщения
@dp.message()
async def send_echo(message: Message):
    await message.answer(text="Не понимаю")


if __name__ == "__main__":
    dp.run_polling(bot)
