import logging
import json

from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from storage import (
    ApplicationStorage,
    CompanyPayerStorage,
    CompanyPecipientStorage,
)
from requests import make_get_request
from keyboards.main_menu import get_menu
from keyboards.application_fields_menu import get_application_fields_menu
from utils import (
    send_message, get_apllications_list, get_company_by_inn
)
from validators import validate_date
from constants import (
    TECH_MESSAGES,
    SERVICE_CHAT_ID,
    EP_APPLICATION,
    GET_PARAM_USER,
    MESSAGES,
    EP_COMPANY_PAYER,
    EP_COMPANY_RECIPIENT,
)

router = Router()
application_storage = ApplicationStorage()
company_payer_storage = CompanyPayerStorage()
company_recipient_storage = CompanyPecipientStorage()


class NewCost(StatesGroup):
    edit_cost = State()


class NewTagetDate(StatesGroup):
    edit_date = State()


async def record_storage(apllication, payer, recipient):
    application_storage.update_application_id(apllication["id"])
    application_storage.update_application_cost(apllication["cost"])
    application_storage.update_target_date(apllication["target_date"])
    company_payer_storage.update_company_name(payer["company_name_payer"])
    company_payer_storage.update_company_inn(payer["company_inn_payer"])
    company_recipient_storage.update_company_name(
        recipient["company_name_recipient"]
    )
    company_recipient_storage.update_company_inn(
        recipient["company_inn_recipient"]
    )


async def print_apllication(message):
    user_message = MESSAGES["application"].format(
            application_storage.application_id,
            application_storage.application_cost,
            application_storage.target_date,
            company_payer_storage.company_name,
            company_payer_storage.company_inn,
            company_recipient_storage.company_name,
            company_recipient_storage.company_inn
        )
    await message.answer(f"Ваша заявка: {user_message}")


@router.message(StateFilter(None), F.text.lower() == "повторить заявку")
async def new_repeat_application(message: Message, state: FSMContext):
    """Обрабатывает клик по кнопке Повторить заявку."""
    tg_user_id = message.from_user.id
    value = GET_PARAM_USER + str(tg_user_id)
    try:
        apllications_list = await get_apllications_list(message, value)
    except Exception as e:
        logging.info(f"Ошибка при получение спиcка заявок: {e}")
        await message.answer(MESSAGES["menu"], reply_markup=get_menu())

    if len(apllications_list) > 0:
        old_apllication = apllications_list[-1]

        inn_payer = str(old_apllication["inn_payer"])
        company_payer = await get_company_by_inn(
            EP_COMPANY_PAYER, inn_payer
        )

        inn_recipient = str(old_apllication["inn_recipient"])
        company_recipient = await get_company_by_inn(
            EP_COMPANY_RECIPIENT, inn_recipient
        )

        await record_storage(old_apllication, company_payer, company_recipient)
        await print_apllication(message)
        await message.answer(
            "Вы можете отредактировать заявку или отправить ее менеджеру:",
            reply_markup=get_application_fields_menu()
        )
        logging.info("Последняя заявка получена")
    else:
        await message.answer("У вас еще нет заявок, создайте новую!")
        await message.answer(MESSAGES["menu"], reply_markup=get_menu())


@router.callback_query(lambda c: c.data == 'edit_cost')
async def get_new_cost(update: types.CallbackQuery, state: FSMContext):
    await state.set_state(NewCost.edit_cost)
    await update.message.answer("Введите новую сумму заявки:")
    logging.info("Редактирование суммы заявки")


@router.message(
    lambda message: message.text.isdigit(),
    NewCost.edit_cost
)
async def edit_cost(message: types.Message, state: FSMContext):
    application_cost = int(message.text)
    application_storage.update_application_cost(application_cost)
    await message.answer(f"Вы ввели сумму заявки: {application_cost}")
    await print_apllication(message)
    await state.set_state(None)
    await message.answer(
        "Отредактируйте или отправьте заявку",
        reply_markup=get_application_fields_menu()
    )
    logging.info("Сумма заявки отредактирована")


@router.message(F.text, NewCost.edit_cost)
async def invalid_values_application_cost(
    message: types.Message,
    state: FSMContext
):
    """Валидация сообщения с суммаой заявки."""
    await message.answer(
        "Внимание! Сумма должна быть числом! Попробуйте еще раз.")
    logging.info("Ошибка редактирования суммы заявки")


@router.callback_query(lambda c: c.data == 'edit_target_date')
async def get_new_target_data(update: types.CallbackQuery, state: FSMContext):
    await state.set_state(NewTagetDate.edit_date)
    await update.message.answer(
        "Введите дату в формате: 20.10.25, не ранее текущего дня."
    )
    logging.info("Редактирование даты")


@router.message(
    lambda message: validate_date(message.text),
    NewTagetDate.edit_date
)
async def edit_target_date(message: types.Message, state: FSMContext):
    application_storage.update_target_date(message.text)
    await message.answer(f"Вы ввели новую дату: {message.text}")
    await print_apllication(message)
    await state.set_state(None)
    await message.answer(
        "Отредактируйте или отправьте заявку",
        reply_markup=get_application_fields_menu()
    )
    logging.info("Дата заявки отредактирована")


@router.message(F.text, NewTagetDate.edit_date)
async def invalid_values_target_date(
    message: types.Message,
    state: FSMContext
):
    """Валидация даты."""
    await message.answer(
        "Вы ввели дату в неправильном формате!")
    await message.answer(
        "Введите дату в формате: 20.10.25, не ранее текущего дня."
    )
    logging.info("Ошибка редактирования суммы заявки")
