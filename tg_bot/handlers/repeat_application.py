import logging
import json

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from storage import ApplicationStorage
from requests import make_get_request
from keyboards.main_menu import get_menu
from utils import send_message, get_apllications_list
from constants import (
    TECH_MESSAGES,
    SERVICE_CHAT_ID,
    EP_APPLICATION,
    GET_PARAM_USER,
    MESSAGES,
)

router = Router()
application_storage = ApplicationStorage()


@router.message(StateFilter(None), F.text.lower() == "повторить заявку")
async def new_repeat_application(message: Message, state: FSMContext):
    """Обрабатывает клик по кнопке Повторить заявку."""
    tg_user_id = message.from_user.id
    value = GET_PARAM_USER + str(tg_user_id)
    try:
        apllications_list = await get_apllications_list(message, value)
    except Exception as e:
        logging.info(f"Ошибка при получение спиcка заявок: {e}")
        await message.answer(MESSAGES["menu"], reply_markup=get_menu())

    if apllications_list:
        await message.answer(f"Ваша последняя заявка: {apllications_list[-1]}")
        logging.info("Последняя заявка получена")
