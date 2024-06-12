import json
import logging

from aiogram import Router, F
from aiogram.types import Message

from requests import (
    make_get_request,
)
from keyboards.main_menu import get_menu
from utils import send_message
from constants import (
    MESSAGES,
    TECH_MESSAGES,
    SERVICE_CHAT_ID,
    EP_COMPANY_PAYER,
)

router = Router()


@router.message(F.text.lower() == "мои юр. лица")
async def answer_no1(message: Message):
    """Обрабатывает клик по кнопке 'мои юр. лица'."""
    logging.info("Пользователь запросил компании")
    tg_id = str(message.from_user.id)
    company_list = False
    try:
        response = await make_get_request(EP_COMPANY_PAYER, tg_id)
        company_list = json.loads(response.text)
    except Exception as e:
        logging.info(f"Ошибка при получение спиcка компаний: {e}")
        await send_message(
            SERVICE_CHAT_ID, f"Ошибка при получение спиcка компаний: {e}"
        )
        await message.answer(TECH_MESSAGES["api_error"])

    if company_list:
        for company in company_list:
            answer = MESSAGES["company"].format(
                company["company_name"],
                company["company_inn"]
            )
            await message.answer(answer)
        logging.info("Пользователь получил список компаний")
    else:
        await message.answer(
            "Создайте первую заявку, для добавления компании."
        )
        logging.info("Пользователь получил список заявок (пустой)")

    await message.answer(MESSAGES["menu"], reply_markup=get_menu())
    logging.info("Пользователь в меню")
