import logging
import json

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message
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

        user_message = MESSAGES["application"].format(
            application_storage.application_id,
            application_storage.application_cost,
            application_storage.target_date,
            company_payer_storage.company_name,
            company_payer_storage.company_inn,
            company_recipient_storage.company_name,
            company_recipient_storage.company_inn
        )

        await message.answer(f"Ваша зявка: {user_message}")
        await message.answer(
            "Вы можете отредактировать заявку или отправить ее менеджеру:",
            reply_markup=get_application_fields_menu()
        )
        logging.info("Последняя заявка получена")
