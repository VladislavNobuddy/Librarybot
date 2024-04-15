from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from typing import Optional
from core.callback.callback import *
import urllib.parse as urlib


main_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📚Поиск книг")],
            [KeyboardButton(text="📖Добавить книгу")],
            [KeyboardButton(text="👤Профиль")],
            [KeyboardButton(text="⚠️FAQ")]
            ], resize_keyboard=True
)

cancel_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙Отмена", callback_data=ServiceCallbackFactory(act='back').pack())]
    ]
)

def genre_and_cancel_kb(genre_list):
    builder = InlineKeyboardBuilder()
    builder_back = InlineKeyboardBuilder()

    for genre in genre_list:
        builder.add(InlineKeyboardButton(
            text=genre, callback_data=ServiceCallbackFactory(genre=genre).pack()
        ))
    builder.adjust(3)

    builder_back.row(InlineKeyboardButton(text='🔙Отмена', callback_data=ServiceCallbackFactory(act='back').pack())) 
    
    builder_back.attach(builder)
    return builder_back.as_markup()

yes_no_kb = InlineKeyboardMarkup(
    inline_keyboard=[
            [InlineKeyboardButton(text="✅Добавить книгу", callback_data=ServiceCallbackFactory(act='add_book').pack())],
            [InlineKeyboardButton(text="❌Отменить действие", callback_data=ServiceCallbackFactory(act='back').pack())]
            ], resize_keyboard=True
)

def book_list_kb(list):
    builder = InlineKeyboardBuilder()

    for item in list:
        builder.add(InlineKeyboardButton(
            text=f'{item[0]}|{item[1]}', callback_data=BookCallbackFactory(name=item[0], book_id=item[2]).pack()
        ))

    builder.adjust(2)

    return builder.as_markup()

book_act = InlineKeyboardMarkup(
    inline_keyboard=[
            [InlineKeyboardButton(text="⬇️Скачать книгу", callback_data=ServiceCallbackFactory(act='add_book').pack())],
            [InlineKeyboardButton(text="❌Отменить действие", callback_data=ServiceCallbackFactory(act='back').pack())]
            ], resize_keyboard=True
)


def book_act(owner, book_id):
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(
        text="⬇️Скачать книгу", callback_data=BookCallbackFactory(act='download', book_id=book_id).pack()))
    
    if owner == True:
        builder.add(InlineKeyboardButton(
        text="❌Удалить книгу", callback_data=BookCallbackFactory(act='delete_book', book_id=book_id).pack()))

    builder.add(InlineKeyboardButton(
        text="🔙Назад", callback_data=ServiceCallbackFactory(act='back').pack()))

    builder.adjust(2)

    return builder.as_markup()