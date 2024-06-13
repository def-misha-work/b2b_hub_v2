import logging
import json

from aiogram import Router, F
from aiogram.types import Message

from keyboards.main_menu import get_menu
from requests import (
    make_get_request,
)
from utils import send_message, get_apllications_list
from constants import (
    MESSAGES,
    TECH_MESSAGES,
    SERVICE_CHAT_ID,
    EP_APPLICATION,
    EP_COMPANY_PAYER,
    EP_COMPANY_RECIPIENT,
    GET_PARAM_USER,
)

router = Router()


@router.message(F.text.lower() == "мои заявки")
async def get_application_list(message: Message):
    """Обрабатывает клик по кнопке Список заявок."""
    tg_user_id = message.from_user.id
    value = GET_PARAM_USER + str(tg_user_id)
    application_list = await get_apllications_list(message, value)

    if application_list:
        for application in application_list:
            response = await make_get_request(
                EP_COMPANY_PAYER,
                application["inn_payer"] + "/"
            )
            if not response.text:
                application["name_payer"] = None
            else:
                name_payer = json.loads(response.text)
                application["name_payer"] = name_payer["company_name_payer"]

            response = await make_get_request(
                EP_COMPANY_RECIPIENT,
                application["inn_recipient"] + "/"
            )
            if not response.text:
                application["name_recipient"] = None
            else:
                name_recipient = json.loads(response.text)
                application["name_recipient"] = name_recipient["company_name_recipient"] # noqa

            answer = MESSAGES["application"].format(
                application["id"],
                application["cost"],
                application["target_date"],
                application["name_payer"],
                application["inn_payer"],
                application["name_recipient"],
                application["inn_recipient"],
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
