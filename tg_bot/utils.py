import json
import logging

from aiogram import Bot
from constants import (
    SERVICE_TELEGRAM_TOKEN,
    SERVICE_CHAT_ID,
    TECH_MESSAGES,
    MESSAGES,
    GET_PARAM_USER,
)
from requests import (
    get_company_name,
    make_get_request
)
from keyboards.company_meny import get_company_menu


service_bot = Bot(token=SERVICE_TELEGRAM_TOKEN)


async def send_message(user_id, text):
    await service_bot.send_message(user_id, text)


async def get_dadata_company_name(inn):
    company_data = await get_company_name(inn)
    company_name = company_data["suggestions"][0]["value"]
    if not company_name:
        await send_message(SERVICE_CHAT_ID, TECH_MESSAGES["company_error"])
        logging.info(TECH_MESSAGES["company_error"])
    return company_name


async def send_user_message(message, text):
    message.answer(text)


async def get_company_list(
    message,
    tg_username,
    endpoint,
    company_name,
    company_inn,
    text,
):
    value = GET_PARAM_USER + str(message.from_user.id)
    try:
        response = await make_get_request(endpoint, value)
        company_list = json.loads(response.text)
    except Exception:
        logging.info(f"@{tg_username} не смог получить список компаний")
        return

    if len(company_list) > 0:
        await message.answer(f"У вас уже есть компании {text}:")
        company_meny = []
        for company in company_list:
            company_text = MESSAGES["company"].format(
                company[company_name],
                company[company_inn]
            )
            company_meny.append(company[company_inn])
            await message.answer(f"{company_text}")
        await message.answer(
            "Нажмите кнопку для выбора:",
            reply_markup=get_company_menu(company_meny)
        )
