import json
import logging

from aiogram import Bot, types
from constants import (
    SERVICE_TELEGRAM_TOKEN,
    SERVICE_CHAT_ID,
    TECH_MESSAGES,
    MESSAGES,
    GET_PARAM_USER,
)
from requests import (
    get_company_name,
    make_get_request,
    make_post_request,
)


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


async def get_company_list(
    answer_func,
    tg_username,
    tg_user_id,
    endpoint,
    company_name,
    company_inn
):
    value = GET_PARAM_USER + str(tg_user_id)
    try:
        response = await make_get_request(endpoint, value)
        company_list = json.loads(response.text)
    except Exception:
        logging.info(f"@{tg_username} не смог получить список компаний")
        return

    if len(company_list) > 0:
        company_meny = []
        for company in company_list:
            company_text = MESSAGES["company"].format(
                company[company_name],
                company[company_inn]
            )
            company_meny.append(company[company_inn])
            await answer_func(f"{company_text}")
        return company_meny


async def extract_inn_from_update(update: types.Message | types.CallbackQuery):
    if isinstance(update, types.Message):
        return update.text
    return update.data


async def get_answer_function(update: types.Message | types.CallbackQuery):
    if isinstance(update, types.Message):
        return update.answer
    return update.message.answer


async def get_company_name_from_dadata(inn_payer, answer_func):
    try:
        company_name = await get_dadata_company_name(inn_payer)
        return company_name
    except Exception:
        await answer_func(TECH_MESSAGES["company_error"])
        return None


async def update_company_in_database(
    inn_payer,
    answer_func,
    endpoint,
    data,
):
    try:
        response = await make_post_request(
            endpoint,
            data
        )
        if response.status_code == 201:
            logging.info("Компании плательщик создана")
        elif response.status_code == 200:
            logging.info("Компании плательщик есть в бд")
    except Exception as e:
        logging.info(f"Ошибка {e} запроса обновления компании")
        await answer_func(TECH_MESSAGES["api_error"])
