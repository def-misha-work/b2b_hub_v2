import logging
import json

from aiogram import Router, F
from aiogram.types import Message

from keyboards.main_menu import get_menu
from requests import (
    make_post_request,
    make_get_request,
)

from utils import get_apllications_list, send_message
from constants import (
    MESSAGES,
    EP_COMPANY_PAYER,
    EP_COMPANY_RECIPIENT,
    GET_PARAM_USER,
    SERVICE_CHAT_ID,
    MANAGER_CHAT_ID,
    ENDPONT_CREATE_USER,
)
from storage import UserStorage


router = Router()


@router.message(F.text.lower() == "мои заявки")
async def get_application_list(message: Message):
    """Обрабатывает клик по кнопке Список заявок."""
    tg_user_id = message.from_user.id

    # TODO костыль убрать после проверки обновления создания юзера.
    tg_username = message.from_user.username
    tg_name = message.from_user.first_name
    tg_surname = message.from_user.last_name
    user_storage = UserStorage(tg_user_id, tg_username, tg_name, tg_surname)
    user_dict = user_storage.to_dict()
    try:
        response = await make_get_request(ENDPONT_CREATE_USER, tg_user_id)
        if response.status_code == 200:
            logging.info("Такой пользователь уже есть")
    except Exception as e:
        logging.info(f"Не удалось получить пользователя: {e}")
        try:
            response = await make_post_request(ENDPONT_CREATE_USER, user_dict)
            if response.status_code == 201:
                logging.info(f"Пользователь создан @{tg_username}")
                logging.info(f"Вся инфа про пользователя: {message.from_user}")
                await send_message(
                    SERVICE_CHAT_ID, f"Новый пользователь @{tg_username}"
                )
                await send_message(
                    MANAGER_CHAT_ID, f"Новый пользователь @{tg_username}"
                )
            else:
                logging.info(f"Пользователь не создан: {response.status_code}")
                logging.info(f"Вся инфа про пользователя: {message.from_user}")
        except Exception as e:
            logging.info(
                f"Ошибка при создании пользователя {tg_username}: {e}"
            )
            logging.info(f"Вся инфа про пользователя: {message.from_user}")
            await send_message(
                SERVICE_CHAT_ID,
                f"Ошибка при создании пользователя {tg_username}: {e}, вся инфа: {message.from_user}"
            )

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
            await message.answer(f"{answer}")
        logging.info(f"Пользователь {tg_user_id} получил список заявок")

        await message.answer(MESSAGES["menu"], reply_markup=get_menu())
        logging.info(f"Пользователь {tg_user_id} в меню")
    else:
        await message.answer("У вас нет активных заявок.")
        logging.info(f"Пользователь {tg_user_id} получил список заявок (пустой)")
        await message.answer(MESSAGES["menu"], reply_markup=get_menu())
        logging.info(f"Пользователь {tg_user_id} в меню")
