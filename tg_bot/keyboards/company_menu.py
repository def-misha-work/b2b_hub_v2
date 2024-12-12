from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_company_menu(data) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for inn in data:
        kb.button(
            text=inn,
            callback_data=inn,
        )
    kb.adjust(3)
    return kb.as_markup()


def get_company_inn_menu(data) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=data, callback_data=data)
    kb.adjust(1)
    return kb.as_markup()
