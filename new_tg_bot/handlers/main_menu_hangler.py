import logging

from aiogram import Router, F, types
from aiogram.filters import StateFilter
# from aiogram.types import Message
from aiogram.fsm.context import FSMContext

# from keyboards.main_menu import get_menu
from states import BotScheme
from constants import (
    INPUT_INN_PAYER_MESSAGE,
)

router = Router()
logger = logging.getLogger(__name__)


@router.message(
    StateFilter(BotScheme.main_menu),
    F.text.lower() == "новая заявка"
)
async def input_inn_payer(message: types.Message, state: FSMContext):
    """
    Старт ветки обработки новой заявки.
    """
    user_data = await state.get_data()
    username = user_data.get('user_username')
    logger.info(f"Пользователь {username} начал создание новой заявки.")
    await message.answer(INPUT_INN_PAYER_MESSAGE)
    await state.set_state(BotScheme.input_inn_payer)
