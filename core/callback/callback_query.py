from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from keyboards.user_kb import *
from core.callback.callback import *
from core.fsm import *
from database.database import DataBase


db = DataBase('database/database.db')
router = Router()


#Сервисные кнопки по типу "назад"
@router.callback_query(ServiceCallbackFactory.filter())
async def callbacks_ServiceCallbackFactory(callback: types.CallbackQuery, callback_data: ServiceCallbackFactory, state:FSMContext):
    match callback_data.act:
        case 'back':
            await state.set_state(state=None)
            with suppress(TelegramBadRequest):
                await callback.message.edit_text('Действие отменено!')

        case 'add_book':
            data = await state.get_data()

            await state.set_state(state=None)
            

            await db.add_new_book(name=data['name'], author=data['author'], adder=callback.from_user.username, adder_id=callback.from_user.id, genre=data['genre'], description=data['description'])

            
            with suppress(TelegramBadRequest):
                await callback.message.edit_text('Книга успешно добавлена!')


    if callback_data.genre:
        await state.update_data(genre=callback_data.genre)
        await state.set_state(Book_fsm.get_description)

        with suppress(TelegramBadRequest):
            await callback.message.edit_text('Жанр успешно получен!\nВведите описание книги\nШаг [4/4]')


@router.callback_query(BookCallbackFactory.filter())
async def callbacks_ServiceCallbackFactory(callback: types.CallbackQuery, callback_data: BookCallbackFactory, state:FSMContext):
    match callback_data.act:
        case 'download':
            with suppress(TelegramBadRequest):
                await callback.message.edit_text('В ТЗ про это ничего не. Просто так добавил, для правдаподобности.', reply_markup=cancel_button)
        
        case 'delete_book':
            await db.delete_book(book_id=callback_data.book_id)
            with suppress(TelegramBadRequest):
                await callback.message.edit_text('Книга успешно удалена!')

        case _:
            book_id = callback_data.book_id

            info = await db.get_info_by_book_id(book_id=book_id)

            if callback.from_user.id == info[0][2]:
                owner = True
            else:
                owner = False
            

            with suppress(TelegramBadRequest):
                await callback.message.edit_text(
f'''
Книга: {callback_data.name}
Автор: {info[0][0]}
Жанр: {info[0][3]}
Описание: {info[0][4]}
------
Добавил: @{info[0][1]}
''', reply_markup=book_act(owner=owner, book_id=book_id))