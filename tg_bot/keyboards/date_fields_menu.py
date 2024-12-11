from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_date_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Сегодня", callback_data="today")
    kb.button(text="Завтра", callback_data="tomorrow")
    kb.button(text="Послезавтра", callback_data="day_after_tomorrow")
    kb.adjust(3)
    return kb.as_markup()
