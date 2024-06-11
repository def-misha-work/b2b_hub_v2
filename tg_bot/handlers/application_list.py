import logging
import json

from aiogram import Router, F
from aiogram.types import Message

from keyboards.main_menu import get_menu
from storage import ApplicationStorage
from requests import (
    make_get_request,
)
from utils import send_message
from constants import (
    MESSAGES,
    TECH_MESSAGES,
    SERVICE_CHAT_ID,
    ENDPONT_GET_APPLICATION_LIST,
)

router = Router()
application_storage = ApplicationStorage()


@router.message(F.text.lower() == "мои заявки")
async def get_application_list(message: Message):
    """Обрабатывает клик по кнопке Список заявок."""
    tg_id = str(message.from_user.id)
    application_list = False
    try:
        response = await make_get_request(ENDPONT_GET_APPLICATION_LIST, tg_id)
        application_list = json.loads(response.text)
    except Exception as e:
        logging.info(f"Ошибка при получение спиcка заявок: {e}")
        await send_message(
            SERVICE_CHAT_ID, f"Ошибка при получение спика заявок: {e}"
        )
        await message.answer(TECH_MESSAGES["api_error"])

    if application_list:
        for application in application_list:
            answer = MESSAGES["application"].format(
                application["id"],
                *application["inn_payer"],
                # application["name_payer"],
                *application["inn_recipient"],
                # application["name_recipient"],
                application["cost"],
                application["target_date"],
            )
            await message.answer(f"Ваши заявки: {answer}")
        logging.info("Пользователь получил список заявок")

        await message.answer(MESSAGES["menu"], reply_markup=get_menu())
        logging.info("Пользователь в меню")
    else:
        await message.answer("У вас нет активных заявок.")
        logging.info("Пользователь получил список заявок (пустой)")
        await message.answer(MESSAGES["menu"], reply_markup=get_menu())
        logging.info("Пользователь в меню")
