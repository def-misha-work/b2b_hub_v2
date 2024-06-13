from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_legal_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Получатели", callback_data="payer")
    kb.button(text="Плательщики", callback_data="recipient")
    kb.adjust(2)
    return kb.as_markup()
