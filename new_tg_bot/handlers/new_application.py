import logging

from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.main_menu import get_menu
from states import BotScheme
from validators import validate_date
# from constants import (

# )

router = Router()
logger = logging.getLogger(__name__)


@router.message(
    StateFilter(None),
    F.text.lower() == "новая заявка"
)
async def create_new_order(
    message: Message,
    state: FSMContext
):
    """
    Запускает цепочку Новая заявка.
    """
    logging.info("Новая заявка")
    await message.answer("Новая заявка")

    # Переходим на следующий шаг.
    await state.set_state(BotScheme.create_inn_payer)


@router.message(
    lambda message: message.text.isdigit() and len(message.text) == 10,
    BotScheme.create_inn_payer
)
async def get_or_create_inn_recipient(
    message: types.Message,
    state: FSMContext
):
    """
    Текстовый ввод!
    Успешно получили ИНН плательщика.
    """
    logging.info("Успешно получили ИНН плательщика")
    await message.answer(message.text)
    await message.answer("Успешно получили ИНН плательщика")

    # Переходим на следующий шаг.
    await state.set_state(BotScheme.create_inn_recipient)


@router.message(
    F.text,
    BotScheme.create_inn_payer
)
async def invalid_inn_payer(
    message: types.Message,
    state: FSMContext
):
    """
    Выдаем ошибку что ИНН получателя, не 10 символов.
    """
    logging.info("Ошибка создания ИНН плательщика")
    await message.answer("Внимание! ИНН плательщика должен содержать 10 цифр!")

    # Возвращаемся на шаг назад.
    await state.set_state(BotScheme.create_inn_payer)


@router.message(
    lambda message: message.text.isdigit() and len(message.text) == 12,
    BotScheme.create_inn_recipient
)
async def get_or_create_inn_payer(
    message: types.Message,
    state: FSMContext
):
    """
    Текстовый ввод!
    Успешно получили ИНН получателя.
    """
    logging.info("Успешно получили ИНН получателя")
    await message.answer(message.text)
    await message.answer("Успешно получили ИНН получателя")

    # Переходим на следующий шаг.
    await state.set_state(BotScheme.create_sum_order)


@router.message(
    F.text,
    BotScheme.create_inn_recipient
)
async def invalid_inn_recipient(
    message: types.Message,
    state: FSMContext
):
    """
    Выдаем ошибку что ИНН получателя, не 12 символов.
    """
    logging.info("Ошибка создания ИНН получателя")
    await message.answer("Внимание! ИНН получателя должен содержать 12 цифр!")

    # Возвращаемся на шаг назад.
    await state.set_state(BotScheme.create_inn_recipient)


@router.message(
    lambda message: message.text.isdigit() and int(message.text) > 99999,
    BotScheme.create_sum_order
)
async def create_sum_order(
    message: types.Message,
    state: FSMContext
):
    """
    Успешное получение суммы заявки.
    """
    logging.info("Получили сумму заявки")
    await message.answer(message.text)
    await message.answer("Получили сумму заявки")

    # Переходим на следующий шаг.
    await state.set_state(BotScheme.create_date_order)


@router.message(
    F.text,
    BotScheme.create_sum_order
)
async def invalid_sum_order(
    message: types.Message,
    state: FSMContext
):
    """
    Выдаем ошибку о неверном вводе суммы заявки.
    """
    logging.info("Внимание! Сумма должна быть числом от 100000!")
    await message.answer("Внимание! Сумма должна быть числом от 100000!")

    # Возвращаемся на шаг назад.
    await state.set_state(BotScheme.create_sum_order)


@router.message(
    lambda message: validate_date(message.text),
    BotScheme.create_date_order
)
async def create_date_order(
    message: types.Message,
    state: FSMContext
):
    """
    Успешное получение даты заявки.
    """
    logging.info("Получили дату заявки")
    await message.answer(message.text)
    await message.answer("Получили дату заявки")

    # Переходим в меню
    await state.set_state(None)
    await message.answer("Заявка отправлена!")
    await message.answer("Вы в меню!", reply_markup=get_menu())


@router.message(
    F.text,
    BotScheme.create_date_order
)
async def invalid_date_order(
    message: types.Message,
    state: FSMContext
):
    """
    Выдаем ошибку о неверном вводе даты заявки.
    """
    logging.info("Внимание! Сумма должна быть числом!")
    await message.answer("Введите дату в формате: 20.10.25, от настоящего дня.")

    # Возвращаемся на шаг назад.
    await state.set_state(BotScheme.create_date_order)
