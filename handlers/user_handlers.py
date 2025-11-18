from copy import deepcopy

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from keyboards.menu_commands import set_book_main_menu, set_default_main_menu
from keyboards.rsp_keyboard import game_kb, yes_no_kb
from keyboards.keyboards import select_game_kb
from keyboards.cube_keyboard import cube_kb, throw_or_back_kb
from lexicon.lexicon_ru import LEXICON_RU
from services.services import get_bot_choice, get_winner
from filters.filters import IsDelBookmarkCallbackData, IsDigitCallbackData
from keyboards.bookmarks_kb import create_bookmarks_keyboard, create_edit_keyboard
from keyboards.pagination_kb import create_pagination_keyboard
from keyboards.book_keyboard import back_to_menu_kb

router = Router()

# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await set_default_main_menu(message.bot, message.chat.id)
    await message.answer(text=LEXICON_RU['/start'], reply_markup=select_game_kb)


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await set_default_main_menu(message.bot, message.chat.id)
    await message.answer(text=LEXICON_RU['/help'], reply_markup=select_game_kb)


# Этот хэндлер срабатывает на согласие пользователя играть в игру камень - ножницы - бумага
@router.message(F.text == LEXICON_RU['rsp_game'])
async def process_yes_answer(message: Message):
    await set_default_main_menu(message.bot, message.chat.id)
    await message.answer(text=LEXICON_RU['yes'], reply_markup=game_kb)

# Этот хэндлер срабатывает на согласие пользователя играть в игру с кубиком
@router.message(F.text == LEXICON_RU['cube_game'])
async def process_yes_answer(message: Message):
    await set_default_main_menu(message.bot, message.chat.id)
    await message.answer(text=LEXICON_RU['yes_cube'], reply_markup=cube_kb)

# Этот хэндлер срабатывает на согласие пользователя открыть книгу
@router.message(F.text == LEXICON_RU['book'])
async def process_yes_answer(message: Message, db: dict):
    await message.answer(text=LEXICON_RU['book_welcome'], reply_markup=back_to_menu_kb)
    await set_book_main_menu(message.bot, message.chat.id)
    if message.from_user.id not in db["users"]:
        db["users"][message.from_user.id] = deepcopy(db.get("user_template"))

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
    await set_default_main_menu(message.bot, message.chat.id)
    await message.answer(text=LEXICON_RU['choose_game_submit'], reply_markup=select_game_kb)

# Этот хэндлер срабатывает при нажатии кнопки "Бросить кубик"
@router.message(F.text == LEXICON_RU['throw_cube'])
async def process_yes_answer(message: Message):
    await message.answer_dice(emoji='🎲', reply_markup=throw_or_back_kb)


# Этот хэндлер срабатывает на любую из игровых кнопок
@router.message(F.text.in_([LEXICON_RU['rock_button'],
                            LEXICON_RU['paper'],
                            LEXICON_RU['scissors']]))
async def process_game_button(message: Message):
    bot_choice = get_bot_choice()
    await message.answer(text=f'{LEXICON_RU["bot_choice"]} '
                              f'- {LEXICON_RU[bot_choice]}')
    winner = get_winner(message.text, bot_choice)
    await message.answer(text=LEXICON_RU[winner], reply_markup=yes_no_kb)

# ------------------ Хэндлеры для книги ---------------------

# Этот хэндлер будет срабатывать на команду "/beginning"
# и отправлять пользователю первую страницу книги с кнопками пагинации
@router.message(Command(commands="beginning"))
async def process_beginning_command(message: Message, book: dict, db: dict):
    db["users"][message.from_user.id]["page"] = 1
    text = book[1]
    await message.answer(
        text=f"<u>{text}</u>",
        reply_markup=create_pagination_keyboard(
            "backward",
            f"1/{len(book)}",
            "forward",
        ),
    )


# этот хэндлер будет срабатывать на команду "/continue"
# и отправлять пользователю страницу книги, на которой пользователь
# остановился в процессе взаимодействия с ботом
@router.message(Command(commands="continue"))
async def process_continue_command(message: Message, book: dict, db: dict):
    text = book[db["users"][message.from_user.id]["page"]]
    await message.answer(
        text=f"<u>{text}</u>",
        reply_markup=create_pagination_keyboard(
            "backward",
            f"{db['users'][message.from_user.id]["page"]}/{len(book)}",
            "forward",
        ),
    )


# этот хэндлер будет срабатывать на команду "/bookmarks"
# и отправлять пользователю список сохраненных закладок,
# если они есть или сообщение о том, что закладок нет
@router.message(Command(commands="bookmarks"))
async def process_bookmarks_command(message: Message, book: dict, db: dict):
    if db["users"][message.from_user.id]["bookmarks"]:
        await message.answer(
            text=LEXICON_RU[message.text],
            reply_markup=create_bookmarks_keyboard(
                *db["users"][message.from_user.id]["bookmarks"], book=book
            ),
        )
    else:
        await message.answer(text=LEXICON_RU["no_bookmarks"])


# этот хэндлер будет срабатывать на нажатие инлайн-кнопки "вперед"
# во время взаимодействия пользователя с сообщением-книгой
@router.callback_query(F.data == "forward")
async def process_forward_press(callback: CallbackQuery, book: dict, db: dict):
    current_page = db["users"][callback. from_user.id]["page"]
    if current_page < len(book):
        db["users"][callback.from_user.id]["page"] += 1
        text = book[current_page + 1]
        await callback.message.edit_text(
            text=f"<u>{text}</u>",
            reply_markup=create_pagination_keyboard(
                "backward",
                f"{current_page + 1}/{len(book)}",
                "forward",
            ),
        )
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "назад"
# во время взаимодействия пользователя с сообщением-книгой
@router.callback_query(F.data == "backward")
async def process_backward_press(callback: CallbackQuery, book: dict, db: dict):
    current_page = db["users"][callback. from_user.id]["page"]
    if current_page > 1:
        db["users"][callback.from_user.id]["page"] -= 1
        text = book[current_page - 1]
        await callback.message.edit_text(
            text=f"<u>{text}</u>",
            reply_markup=create_pagination_keyboard(
                "backward",
                f"{current_page - 1}/{len(book)}",
                "forward",
            ),
        )
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с номером текущей страницы и добавлять текущую страницу в закладки
@router.callback_query(
    lambda x: "/" in x.data and x.data.replace("/", "").isdigit()
)
async def process_page_press(callback: CallbackQuery, db: dict):
    db["users"][callback. from_user.id]["bookmarks"].add(
        db["users"][callback. from_user.id]["page"]
    )
    await callback.answer("Страница добавлена в закладки!")


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок
@router.callback_query(IsDigitCallbackData())
async def process_bookmark_press(callback: CallbackQuery, book: dict, db: dict):
    text = book[int(callback.data)]
    db["users"][callback. from_user.id]["page"] = int(callback.data)
    await callback.message. edit_text(
        text=f"<u>{text}</u>",
        reply_markup=create_pagination_keyboard(
            "backward",
            f"{db['users'][callback.from_user.id]['page']}/{len(book)}",
            "forward",
        ),
    )


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "редактировать" под списком закладок
@router. callback_query(F.data == "edit_bookmarks")
async def process_edit_press(callback: CallbackQuery, book: dict, db: dict):
    await callback.message. edit_text(
        text=LEXICON_RU[callback.data],
        reply_markup=create_edit_keyboard(
            *db["users"][callback. from_user.id]["bookmarks"], book=book
        ),
    )


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "отменить" во время работы со списком закладок (просмотр и редактирование)
@router.callback_query(F.data == "cancel")
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON_RU["cancel_text"])


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок к удалению
@router.callback_query(IsDelBookmarkCallbackData())
async def process_del_bookmark_press(callback: CallbackQuery, book: dict, db: dict):
    db["users"][callback.from_user. id]["bookmarks"].remove(int(callback.data[:-3]))
    if db["users"][callback.from_user.id]["bookmarks"]:
        await callback.message.edit_text(
            text=LEXICON_RU["/bookmarks"],
            reply_markup=create_edit_keyboard(
                *db["users"][callback.from_user.id]["bookmarks"], book=book

            ),
        )
    else:
        await callback.message.edit_text(text=LEXICON_RU["no_bookmarks"])