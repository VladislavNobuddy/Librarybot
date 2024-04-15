from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.filters.command import Command, CommandObject
from aiogram.filters.callback_data import CallbackData
from aiogram.types import FSInputFile
from aiogram import F
from main import bot
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from database.database import DataBase
from keyboards.user_kb import *
from core.fsm import *
from utilites import cfg    
from aiogram import Bot
from aiogram.filters import Command


bot = Bot(token=cfg.TOKEN)
router = Router()
db = DataBase('database/database.db')


#главное меню
@router.message(lambda message: message.text == "🔙Назад")
@router.message(Command("start"))
@router.message(lambda message: message.text == "start")
async def menu(message: Message, state: FSMContext):
    await state.set_state(state=None)

    id = message.from_user.id
    is_user_in_db = await db.is_user_in_db(id=id)

    match is_user_in_db:
        case False:
            await db.new_user(id=id)

            await message.answer(f'Привет, <b>{message.from_user.full_name}</b>!\nБот-библиотека к твоим услугам!' #pythonic
                                + '\nПоходу ты тут впервые... Рекомендую начать с раздела ⚠️FAQ', parse_mode='HTML', reply_markup=main_menu)
        
        case True:
            await message.answer(f'Привет, <b>{message.from_user.full_name}</b>!\nБот-библиотека к твоим услугам!' #pythonic
                                + '\nРады видеть тебя вновь!❤️', parse_mode='HTML', reply_markup=main_menu)


#раздел faq
@router.message(F.text == "⚠️FAQ")
async def faq(message: Message):
    await message.answer(
'''
Давай представим, что здесь описание сервиса, ссылки на чаты, ну ты пон крч.
бла-бла-бла
/genre (жанр)", чтобы искать книги по жанру
''', reply_markup=main_menu)
    

@router.message(F.text == "📖Добавить книгу")
async def adding_book(message: Message, state: FSMContext):
    mes = await message.answer('Введите желаемое название для книги\nШаг [1/4]', reply_markup=cancel_button) #См. 67 строчку

    await state.update_data(data={'mes_to_change':mes}) #словарем чисто, чтобы повыёбываться. дальше - по-человечески
    await state.set_state(state=Book_fsm.get_name)

#Че за Cancel_button? keyboards/user_kb.py 18 строчка - объявление. Обработка в utilites/callback.py

@router.message(Book_fsm.get_name)
async def add_book_name(message: Message, state: FSMContext):
    data = await state.get_data()
    mes = data['mes_to_change']

    await state.update_data(name=message.text)
    await state.set_state(state=Book_fsm.get_author)

    await message.delete()
    with suppress(TelegramBadRequest):
        await mes.edit_text('Название успешно получено!\nВведите автора книги\nШаг [2/4]', reply_markup=cancel_button)


@router.message(Book_fsm.get_author)
async def add_book_author(message: Message, state: FSMContext):
    data = await state.get_data()
    mes = data['mes_to_change']

    await state.update_data(author=message.text)
    await state.set_state(state=Book_fsm.get_genre)

    await message.delete()

    genre_list = await db.genre_list()
    with suppress(TelegramBadRequest):
        await mes.edit_text('Автор успешно получен!\nВведите жанр книги или выберите из предложенных\nШаг [3/4]', reply_markup=genre_and_cancel_kb(genre_list=genre_list))


@router.message(Book_fsm.get_genre)
async def add_book_description(message: Message, state: FSMContext):
    data = await state.get_data()
    mes = data['mes_to_change']

    await state.set_state(Book_fsm.get_description)

    try:
        data['genre']

    except KeyError:
        await message.delete()
        await state.update_data(genre=message.text)
    
    with suppress(TelegramBadRequest):
        await mes.edit_text('Жанр успешно получен!\nВведите описание книги\nШаг [4/4]', reply_markup=cancel_button)

    
@router.message(Book_fsm.get_description)
async def add_book_question(message: Message, state: FSMContext):
    data = await state.get_data()
    mes = data['mes_to_change']


    await state.set_state(Book_fsm.get_confirm)
    await state.update_data(description=message.text)

    await message.delete()    
    with suppress(TelegramBadRequest):
        await mes.edit_text(f'''
Описание успешно получено!
Добавить книгу?
Сейчас она выглядит следующим образом:
<b>Название:</b> {data['name']}
<b>Автор:</b> {data['author']}
<b>Жанр:</b> {data['genre']}
<b>Описание:</b> {message.text}
''', parse_mode='HTML', reply_markup=yes_no_kb)


@router.message(Book_fsm.get_confirm, F.text == "✅Добавить книгу")
async def add_book(message: Message, state: FSMContext):
    data = await state.get_data()

    await state.set_state(state=None)
    
    await db.add_new_book(name=data['name'], author=['author'], adder=message.from_user.username, adder_id=message.from_user.id, genre=data['genre'], description=data['description'])

    await message.answer('Книга успешно добавлена!')


@router.message(Book_fsm.get_confirm, F.text == "❌Отменить действие")
async def add_book(message: Message, state: FSMContext):
    await state.set_state(state=None)

    await message.answer('Добавление книги отменено', reply_markup=main_menu)


@router.message(F.text == "📚Поиск книг")
async def book_list_func(message: Message, state: FSMContext):
    await message.answer('⚙️Загружаем книги...', reply_markup=cancel_button)

    book_list = await db.get_book_list()
    await state.set_state(state=Book_fsm.search_book)

    await message.answer('Выберите книгу ниже или введите ключевое слово для поиска', reply_markup=book_list_kb(list=book_list))


@router.message(Command('genre'))
async def filter_by_genre_func(message: Message, command: CommandObject):
    args = command.args

    book_list = await db.get_book_list()

    books_by_genre = []

    for book in book_list:
        if args in book[3]:
            books_by_genre.append(book)

    await message.answer(f'🔎Поиск по жанру "{message.text}"', reply_markup=book_list_kb(books_by_genre))
    


@router.message(Book_fsm.search_book)
async def add_book(message: Message, state: FSMContext):
    book_list = await db.get_book_list()

    books_by_key = []

    for book in book_list:
        if message.text in book[0] or message.text in book[1]:
            books_by_key.append(book)

    await message.answer(f'🔎Поиск по запросу "{message.text}"', reply_markup=book_list_kb(books_by_key))
