import logging
import json

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from storage import ApplicationStorage
from requests import (
    make_get_request,
)
from utils import send_message
from constants import (
    TECH_MESSAGES,
    SERVICE_CHAT_ID,
    ENDPONT_GET_APPLICATION_LIST,
)

router = Router()
application_storage = ApplicationStorage()


@router.message(StateFilter(None), F.text.lower() == "повторить заявку")
async def application_repeat(message: Message, state: FSMContext):
    """Обрабатывает клик по кнопке Повторить заявку."""
    tg_id = str(message.from_user.id)
    try:
        response = await make_get_request(ENDPONT_GET_APPLICATION_LIST, tg_id)
    except Exception as e:
        logging.info(f"Ошибка при получение спиcка заявок: {e}")
        await send_message(
            SERVICE_CHAT_ID, f"Ошибка при получение спика заявок: {e}"
        )
        await message.answer(TECH_MESSAGES["api_error"])
    logging.info(f"Ответ с заявками {response.text}")
    logging.info(f"Ответ с заявками {type(response.text)}")
    last_application = json.loads(response.text)
    await message.answer(f"Ваша последняя заявка: {last_application[-1]}")
