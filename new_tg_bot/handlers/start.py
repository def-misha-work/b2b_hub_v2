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

    user_name = message.from_user.first_name
    logger.info(f"Это ответ ТГ: {message.from_user}")
    if user_name:
        await message.answer(START_MESSAGE.format(user_name))
        await message.answer("Вы в меню!", reply_markup=get_menu())

    if not user_name:
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
