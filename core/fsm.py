from aiogram.fsm.state import State, StatesGroup

class Book_fsm(StatesGroup):
    get_name = State()
    get_author = State()
    get_genre = State()
    get_description = State()
    get_confirm = State()
    search_book = State()
