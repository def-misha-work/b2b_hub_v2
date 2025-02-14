import logging

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import BotScheme
from keyboards.main_menu import get_menu
from constants import (
    START_MESSAGE,
    NO_USER_NAME,
)

router = Router()

logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Запускает бота по команде /start. Выводит меню.
    Отправляет в БД запрос на создание юзера."""
    logger.info("Пользователь нажал на старт")
    await state.set_state(None)

    # Поля для проверки
    logger.info(f"Это все что в message.from_user: {message.from_user}")

    user_id = message.from_user.id
    first_name = message.from_user.first_name
    username = message.from_user.username
    logger.info(f"Имя пользователя: {user_id}")
    logger.info(f"Имя пользователя: {first_name}")
    logger.info(f"Имя пользователя: {username}")
    # TODO сделать проверку в базе что
    # пользователь есть или создать его если нет.
    if first_name:
        await message.answer(START_MESSAGE.format(first_name))
        await message.answer("Вы в меню!", reply_markup=get_menu())

    if not first_name:
        await message.answer(NO_USER_NAME)
        await state.set_state(BotScheme.no_user_name)


@router.message(
    F.text,
    BotScheme.no_user_name
)
async def no_user_name(
    message: types.Message,
    state: FSMContext
):
    """Получает имя пользователя если у него скрыто поле first_name."""
    ...
    # user_name = message.text
    # TODO дописать после создания юзера.
