from aiogram.filters.callback_data import CallbackData
from typing import Optional


class ServiceCallbackFactory(CallbackData, prefix="settings"):
    act: Optional[str] = None
    genre: Optional[str] = None

class BookCallbackFactory(CallbackData, prefix="book_callb"):
    name: Optional[str] = None
    book_id: Optional[int] = None
    act: Optional[str] = None

#обработка колбэков в callback_query.py этой же директории
                