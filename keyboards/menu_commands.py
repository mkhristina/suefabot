from aiogram import Bot
from aiogram. types import BotCommand, BotCommandScopeChat

from lexicon.lexicon_ru import LEXICON_COMMANDS_BOOK, LEXICON_COMMANDS


# Функция для настройки кнопки Menu бота
async def set_book_main_menu(bot: Bot, chat_id: int):
    main_menu_commands = [
        BotCommand(command=command, description=description)
        for command, description in LEXICON_COMMANDS_BOOK.items()
    ]
    await bot.set_my_commands(
        commands=main_menu_commands,
        scope=BotCommandScopeChat(chat_id=chat_id)
    )


# Функция для настройки кнопки Menu бота
async def set_default_main_menu(bot: Bot, chat_id: int):
    main_menu_commands = [
        BotCommand(command=command, description=description)
        for command, description in LEXICON_COMMANDS.items()
    ]
    await bot.set_my_commands(
        commands=main_menu_commands,
        scope=BotCommandScopeChat(chat_id=chat_id)
    )