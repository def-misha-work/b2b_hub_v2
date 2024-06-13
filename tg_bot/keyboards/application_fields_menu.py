from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_application_fields_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Сумму заявки", callback_data="edit_cost")
    kb.button(text="Дату выполнения", callback_data="edit_target_date")
    kb.button(text="Получателя", callback_data="edit_payer")
    kb.button(text="Плательщика", callback_data="edit_recipient")
    kb.button(text="Отправить заявку", callback_data="send_apllication")
    kb.adjust(2)
    return kb.as_markup()
