import logging

from aiogram import Router, F, types
from aiogram.filters import StateFilter
# from aiogram.types import Message
from aiogram.fsm.context import FSMContext

# from keyboards.main_menu import get_menu
from states import BotScheme
# from constants import (
#     INPUT_INN_PAYER_MESSAGE,
# )

router = Router()
logger = logging.getLogger(__name__)


@router.message(
    StateFilter(BotScheme.input_inn_payer),
    lambda message: message.text.isdigit() and len(message.text) == 10,
)
async def input_text_inn_payer(message: types.Message, state: FSMContext):
    """
    Обработка ИНН плательщика.
    """
    inn = int(message.text)
    user_data = await state.get_data()
    username = user_data.get('user_username')
    logger.info(
        f"Пользователь {username} ввел ИНН плательщика: {inn}."
    )
    logger.info(type(inn))
    await message.answer(f"Вы ввели: {inn}")
    # Сохраняем введенные данные
    await state.update_data(inn_payer=inn)
    # Переводим на следущий шаг
    await state.set_state(BotScheme.input_inn_recipient)


@router.message(
    F.text,
    BotScheme.input_inn_payer
)
async def invalid_input_inn_payer(
    message: types.Message,
    state: FSMContext
):
    """
    Выдаем ошибку что ИНН получателя, не 10 символов.
    """
    user_data = await state.get_data()
    username = user_data.get('user_username')
    logging.info(f"{username} ошибка создания ИНН плательщика")
    await message.answer("Внимание! ИНН плательщика должен содержать 10 цифр!")
    # Возвращаемся на шаг назад.
    await state.set_state(BotScheme.input_inn_payer)
