import logging
import json

from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from keyboards.main_menu import get_menu
from keyboards.company_menu import get_company_menu

from requests import (
    make_post_request,
)
from storage import (
    ApplicationStorage,
    CompanyPayerStorage,
    CompanyPecipientStorage,
    UserStorage,
)
from utils import (
    send_message,
    get_company_list,
    extract_inn_from_update,
    get_answer_function,
    get_company_name_from_dadata,
    update_company_in_database,
)
from validators import validate_date
from constants import (
    MESSAGES,
    TECH_MESSAGES,
    SERVICE_CHAT_ID,
    MESSAGES_TO_MANAGER,
    MANAGER_CHAT_ID,
    EP_COMPANY_PAYER,
    EP_COMPANY_RECIPIENT,
    EP_APPLICATION,
    ENDPONT_CREATE_USER,
)


router = Router()
application_storage = ApplicationStorage()
company_payer_storage = CompanyPayerStorage()
company_recipient_storage = CompanyPecipientStorage()


class NewApplication(StatesGroup):
    step_1 = State()
    step_2 = State()
    step_3 = State()
    step_4 = State()


@router.message(StateFilter(None), F.text.lower() == "новая заявка")
async def start_new_application(message: Message, state: FSMContext):
    """Обрабатывает клик по кнопке и запускает цепочку Новая заявка."""
    tg_username = message.from_user.username
    tg_user_id = message.from_user.id
    # TODO костыль убрать после проверки обновления создания юзера.
    tg_name = message.from_user.first_name
    tg_surname = message.from_user.last_name
    user_storage = UserStorage(tg_user_id, tg_username, tg_name, tg_surname)
    user_dict = user_storage.to_dict()
    try:
        response = await make_post_request(ENDPONT_CREATE_USER, user_dict)
        if response.status_code == 201:
            logging.info(f"Пользователь создан @{tg_username}")
            logging.info(f"Вся инфа про пользователя: {message.from_user}")
            await send_message(
                SERVICE_CHAT_ID, f"Новый пользователь @{tg_username}"
            )
            await send_message(
                MANAGER_CHAT_ID, f"Новый пользователь @{tg_username}"
            )
        else:
            logging.info(f"Пользователь не создан: {response.status_code}")
            logging.info(f"Вся инфа про пользователя: {message.from_user}")
    except Exception as e:
        logging.info(f"Ошибка при создании пользователя {tg_username}: {e}")
        logging.info(f"Вся инфа про пользователя: {message.from_user}")
        await send_message(
            SERVICE_CHAT_ID,
            f"Ошибка при создании пользователя {tg_username}: {e}, вся инфа: {message.from_user}"
        )
    # конец костыля
    await state.set_state(NewApplication.step_1)
    logging.info(f"@{tg_username} начал создание новой заявки")
    await message.answer(MESSAGES["step1"])
    company_menu = await get_company_list(
        message.answer,
        tg_username,
        tg_user_id,
        EP_COMPANY_PAYER,
        "company_name_payer",
        "company_inn_payer",
    )
    if company_menu:
        await message.answer(
            "Нажмите кнопку для выбора или введите новый ИНН:",
            reply_markup=get_company_menu(company_menu)
        )


@router.message(
    lambda message: message.text.isdigit() and len(message.text) == 10,
    NewApplication.step_1
)
@router.callback_query(
    lambda callback: callback.data.isdigit() and len(callback.data) == 10,
    NewApplication.step_1
)
async def process_inn_payer(
    update: types.Message | types.CallbackQuery,
    state: FSMContext
):
    """Обработка сообщения с ИНН плательщика."""
    inn_payer = await extract_inn_from_update(update)
    answer_func = await get_answer_function(update)
    tg_user_id = update.from_user.id
    tg_username = update.from_user.username

    company_payer_storage.update_tg_id(tg_user_id)
    company_payer_storage.update_company_inn(inn_payer)
    await answer_func(f"Вы ввели ИНН плательщика: {inn_payer}")
    company_name = await get_company_name_from_dadata(inn_payer, answer_func)
    if company_name:
        await answer_func(f"Название вашей компании: {company_name}")
        company_payer_storage.update_company_name(company_name)

    await update_company_in_database(
        inn_payer,
        answer_func,
        EP_COMPANY_PAYER,
        company_payer_storage.to_dict(),
    )

    await answer_func(MESSAGES["step2"])
    company_meny = await get_company_list(
        answer_func,
        tg_username,
        tg_user_id,
        EP_COMPANY_RECIPIENT,
        "company_name_recipient",
        "company_inn_recipient",
    )
    if company_meny:
        await answer_func(
            "Нажмите кнопку для выбора или введите новый ИНН:",
            reply_markup=get_company_menu(company_meny)
        )
    await state.set_state(NewApplication.step_2)
    logging.info("Успех шаг 1")


@router.message(F.text, NewApplication.step_1)
async def invalid_values_inn_payer(message: types.Message, state: FSMContext):
    """Валидация сообщения с числом из 10 символов."""
    await message.answer("Внимание! ИНН организации должен содержать 10 цифр!")
    await message.answer(MESSAGES["step1"])
    await state.set_state(NewApplication.step_1)
    logging.info("Ошибка на шаге 1")


# Обработка inn_recipient step_2
@router.message(
    lambda message: message.text.isdigit() and len(message.text) == 12,
    NewApplication.step_2
)
@router.callback_query(
    lambda callback: callback.data.isdigit() and len(callback.data) == 12,
    NewApplication.step_2
)
async def process_inn_recipient(
    update: types.Message | types.CallbackQuery,
    state: FSMContext
):
    """Обработка сообщения с числом из ровно 12 символов."""
    inn_recipient = await extract_inn_from_update(update)
    answer_func = await get_answer_function(update)
    tg_user_id = update.from_user.id

    company_recipient_storage.update_tg_id(tg_user_id)
    company_recipient_storage.update_company_inn(inn_recipient)
    await answer_func(f"Вы ввели ИНН получателя: {inn_recipient}")
    company_name = await get_company_name_from_dadata(
        inn_recipient,
        answer_func
    )
    if company_name:
        await answer_func(f"Название вашей компании: {company_name}")
        company_recipient_storage.update_company_name(company_name)
    await update_company_in_database(
        inn_recipient,
        answer_func,
        EP_COMPANY_RECIPIENT,
        company_recipient_storage.to_dict(),
    )
    await answer_func(MESSAGES["step3"])
    await state.set_state(NewApplication.step_3)
    logging.info("Успех шаг 2")


@router.message(F.text, NewApplication.step_2)
async def invalid_values_inn_recipient(
    message: types.Message,
    state: FSMContext
):
    """Валидация сообщения с числом из 12 символов."""
    await message.answer("Внимание! ИНН ИП должен содержать 12 цифр!")
    await message.answer(MESSAGES["step2"])
    await state.set_state(NewApplication.step_2)
    logging.info("Ошибка на шаге 2")


# Обработка application_cost step_3
@router.message(
    lambda message: message.text.isdigit(),
    NewApplication.step_3
)
async def get_application_cost(message: types.Message, state: FSMContext):
    """Обработка сообщения с суммой заявки."""
    application_cost = int(message.text)
    application_storage.update_application_cost(application_cost)
    await message.answer(f"Вы ввели сумму заявки: {application_cost}")
    await message.answer(MESSAGES["step4"])
    await state.set_state(NewApplication.step_4)
    logging.info("Успех шаг 3")


@router.message(F.text, NewApplication.step_3)
async def invalid_values_application_cost(
    message: types.Message,
    state: FSMContext
):
    """Валидация сообщения с суммаой заявки."""
    await message.answer("Внимание! Сумма должна быть числом!")
    await message.answer(MESSAGES["step3"])
    await state.set_state(NewApplication.step_3)
    logging.info("Ошибка на шаге 3")


# Обработка target_date step_4
@router.message(
    lambda message: validate_date(message.text),
    NewApplication.step_4
)
async def get_target_date(message: types.Message, state: FSMContext):
    """Обработка сообщения с датой в формате 20.10.25."""
    tg_username = message.from_user.username
    application_id = False

    application_storage.update_tg_id(message.from_user.id)
    application_storage.update_target_date(message.text)
    data_dict = application_storage.to_dict()
    data_dict["inn_payer"] = company_payer_storage.company_inn
    data_dict["inn_recipient"] = company_recipient_storage.company_inn

    # сохраняем в бд
    try:
        response = await make_post_request(
            EP_APPLICATION, data_dict
        )
        data = json.loads(response.text)
        application_id = data["id"]
    except Exception as e:
        logging.info(f"Ошибка при создании заявки: {e}")
        await send_message(SERVICE_CHAT_ID, f"Ошибка создания заявки {e}")
        await message.answer(TECH_MESSAGES["api_error"])
        await state.set_state(None)
        await message.answer(MESSAGES["menu"], reply_markup=get_menu())
        logging.info(f"Пользователь {tg_username} в меню")

    # Отправляем в саппорт и менеджеру
    if application_id:
        application_message = MESSAGES["application"].format(
            application_id,
            application_storage.application_cost,
            application_storage.target_date,
            company_payer_storage.company_name,
            company_payer_storage.company_inn,
            company_recipient_storage.company_name,
            company_recipient_storage.company_inn
        )
        message_manager = MESSAGES_TO_MANAGER["application_created"].format(
            message.from_user.first_name,
            message.from_user.username,
            application_message
        )
        message_user = MESSAGES["application_created"].format(
            application_message
        )
        await send_message(SERVICE_CHAT_ID, message_manager)
        await send_message(MANAGER_CHAT_ID, message_manager)

        await message.answer(message_user)

    application_storage.clear_data()
    company_payer_storage.clear_data()
    company_recipient_storage.clear_data()
    await state.set_state(None)
    await message.answer(MESSAGES["menu"], reply_markup=get_menu())
    logging.info(f"Пользователь {tg_username} в меню")
    logging.info("Успех шаг 4")


@router.message(F.text, NewApplication.step_4)
async def invalid_values_target_date(
    message: types.Message,
    state: FSMContext
):
    """Валидация даты."""
    await message.answer(
        "Введите дату в формате: 20.10.25, не ранее текущего дня."
    )
    await message.answer(MESSAGES["step4"])
    await state.set_state(NewApplication.step_4)
    logging.info("Ошибка на шаге 4")
