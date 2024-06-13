import json
import logging

from aiogram import Router, F, types
from aiogram.types import Message

from requests import make_get_request
from keyboards.main_menu import get_menu
from keyboards.legal_meny import get_legal_menu
from utils import send_message, get_company_list
from constants import (
    MESSAGES,
    TECH_MESSAGES,
    SERVICE_CHAT_ID,
    EP_COMPANY_PAYER,
    EP_COMPANY_RECIPIENT,
    GET_PARAM_USER,
)

router = Router()


@router.message(F.text.lower() == "мои юр. лица")
async def answer_no1(message: Message):
    """Обрабатывает клик по кнопке 'мои юр. лица'."""
    logging.info("Пользователь запросил компании")
    await message.answer("Выберите категорию:", reply_markup=get_legal_menu())


@router.callback_query(lambda c: c.data == 'payer')
async def process_inn_payer(update: types.CallbackQuery):
    await get_company_list(
        update.message.answer,
        update.from_user.username,
        update.from_user.id,
        EP_COMPANY_PAYER,
        "company_name_payer",
        "company_inn_payer",
    )
    await update.message.answer(MESSAGES["menu"], reply_markup=get_menu())


@router.callback_query(lambda c: c.data == 'recipient')
async def process_inn_recipient(update: types.CallbackQuery):
    await get_company_list(
        update.message.answer,
        update.from_user.username,
        update.from_user.id,
        EP_COMPANY_RECIPIENT,
        "company_name_recipient",
        "company_inn_recipient",
    )
    await update.message.answer(MESSAGES["menu"], reply_markup=get_menu())
