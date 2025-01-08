import logging

from aiogram import Router, F, types
from aiogram.types import Message

from keyboards.main_menu import get_menu
from keyboards.legal_menu import get_legal_menu
from utils import get_company_list, send_message
from constants import (
    MESSAGES,
    EP_COMPANY_PAYER,
    EP_COMPANY_RECIPIENT,
    ENDPONT_CREATE_USER,
    SERVICE_CHAT_ID,
    MANAGER_CHAT_ID,
)
from storage import UserStorage
from requests import (
    make_post_request,
    make_get_request,
)


router = Router()


@router.message(F.text.lower() == "мои юр. лица")
async def answer_no1(message: Message):
    """Обрабатывает клик по кнопке 'мои юр. лица'."""
    logging.info("Пользователь запросил компании")
    tg_user_id = message.from_user.id
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

    await message.answer("Выберите категорию:", reply_markup=get_legal_menu())


@router.callback_query(lambda c: c.data == "recipient")
async def process_inn_payer(update: types.CallbackQuery):
    await get_company_list(
        update.message.answer,
        update.from_user.username,
        update.from_user.id,
        EP_COMPANY_PAYER,
        "company_name_payer",
        "company_inn_payer",
    )
    await update.message.answer(MESSAGES["menu"], reply_markup=get_menu())


@router.callback_query(lambda c: c.data == "payer")
async def process_inn_recipient(update: types.CallbackQuery):
    await get_company_list(
        update.message.answer,
        update.from_user.username,
        update.from_user.id,
        EP_COMPANY_RECIPIENT,
        "company_name_recipient",
        "company_inn_recipient",
    )
    await update.message.answer(MESSAGES["menu"], reply_markup=get_menu())
