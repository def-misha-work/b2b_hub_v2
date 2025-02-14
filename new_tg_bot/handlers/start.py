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
    MAIN_MENU_MESSAGE,
    DOMANE_NAME,
)
from api.tg_users_api import ApiTelegramUserRepository


router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Запускает бота по команде /start. Выводит меню.
    Отправляет в БД запрос на создание юзера."""
    # Сбрасываем прошлые состояния, данные
    await state.clear()

    user_id = message.from_user.id
    first_name = message.from_user.first_name
    username = message.from_user.username
    logger.info(f"ID пользователя: {user_id}")
    logger.info(f"Имя пользователя: {first_name}")
    logger.info(f"Ник пользователя: {username}")
    # Сохраняем в словарь state данные пользователя
    await state.update_data(
        user_user_id=user_id,
        user_username=username,
        user_first_name=first_name,
    )

    # проверяем в базе!
    tg_user_in_db = ApiTelegramUserRepository(DOMANE_NAME)
    tg_user_in_db.get_user_by_id("user_id")
    # TODO тут както придумать проверку на поля имя и юзернеим
    if tg_user_in_db is not None:
        await message.answer(f'С возвращением {first_name}')

    if first_name:
        await message.answer(START_MESSAGE.format(first_name))
        await state.set_state(BotScheme.main_menu)
        await message.answer(MAIN_MENU_MESSAGE, reply_markup=get_menu())

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
