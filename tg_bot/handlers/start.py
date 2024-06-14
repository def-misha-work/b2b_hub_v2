import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from storage import UserStorage

from keyboards.main_menu import get_menu
from requests import make_post_request
from utils import send_message
from constants import (
    MESSAGES,
    ENDPONT_CREATE_USER,
    SERVICE_CHAT_ID,
    MANAGER_CHAT_ID
)

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Запускает бота по команде /start. Выводит меню.
    Отправляет в БД запрос на создание юзера."""
    logging.info("Пользователь запустил бота")
    await state.set_state(None)

    tg_id = str(message.from_user.id)
    tg_username = message.from_user.username
    tg_name = message.from_user.first_name
    tg_surname = message.from_user.last_name
    user_storage = UserStorage(tg_id, tg_username, tg_name, tg_surname)
    user_dict = user_storage.to_dict()

    try:
        response = await make_post_request(ENDPONT_CREATE_USER, user_dict)
        if response.status_code == 201:
            logging.info(f"Пользователь создан @{tg_username}")
            await send_message(
                SERVICE_CHAT_ID, f"Новый пользователь @{tg_username}"
            )
            await send_message(
                MANAGER_CHAT_ID, f"Новый пользователь @{tg_username}"
            )
        else:
            logging.info(f"Пользователь не создан: {response.status_code}")
    except Exception as e:
        logging.info(f"Ошибка при создании пользователя: {e}")
        await send_message(
            SERVICE_CHAT_ID,
            f"Ошибка при создании пользователя: {e}"
        )

    await message.answer(MESSAGES["start"].format(tg_name))
    await message.answer(MESSAGES["menu"], reply_markup=get_menu())
    logging.info(f"Пользователь {tg_username} в меню")
