import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from aiogram.fsm.context import FSMContext
from keyboards.main_menu import get_menu
from constants import (
    START_MESSAGE,
)

router = Router()

logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Запускает бота по команде /start. Выводит меню.
    Отправляет в БД запрос на создание юзера."""
    logger.info("Пользователь нажал на старт")
    tg_username = message.from_user.username
    await state.set_state(None)
    await message.answer(START_MESSAGE.format(tg_username))
    await message.answer("Вы в меню!", reply_markup=get_menu())
