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
    UserStorage,
)
from keyboards.main_menu import get_menu
from keyboards.company_menu import (
    get_company_menu,
    get_company_inn_menu,
)
from keyboards.application_fields_menu import get_application_fields_menu
from keyboards.date_fields_menu import get_date_menu
from requests import make_post_request
from utils import (
    send_message,
    get_apllications_list,
    get_company_by_inn,
    new_get_company_list,
    get_company_list,
    extract_inn_from_update,
    get_answer_function,
    get_company_name_from_dadata,
    update_company_in_database,
    get_date,
)
from validators import validate_date
from constants import (
    GET_PARAM_USER,
    MESSAGES,
    EP_COMPANY_PAYER,
    EP_COMPANY_RECIPIENT,
    EP_APPLICATION,
    SERVICE_CHAT_ID,
    TECH_MESSAGES,
    MESSAGES_TO_MANAGER,
    MANAGER_CHAT_ID,
    ENDPONT_CREATE_USER,
)

router = Router()
application_storage = ApplicationStorage()
company_payer_storage = CompanyPayerStorage()
company_recipient_storage = CompanyPecipientStorage()

COMPANY_LIST_ALL = []


class NewCost(StatesGroup):
    edit_cost = State()


class NewTagetDate(StatesGroup):
    edit_date = State()


class NewPayer(StatesGroup):
    edit_payer = State()


class NewRecipient(StatesGroup):
    edit_recipient = State()


async def record_storage(apllication, payer, recipient):
    logging.info("Обновление all storage")
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
    logging.info("Вывод заявки")
    user_message = MESSAGES["application_repeat"].format(
            application_storage.application_cost,
            application_storage.target_date,
            company_payer_storage.company_name,
            company_payer_storage.company_inn,
            company_recipient_storage.company_name,
            company_recipient_storage.company_inn
        )
    await message(
        f"Заявка: {user_message}"
    )


@router.message(StateFilter(None), F.text.lower() == "повторить заявку")
async def new_repeat_application(message: Message, state: FSMContext):
    """Обрабатывает клик по кнопке Повторить заявку."""
    logging.info("Пользователь повторяет заявку")
    tg_user_id = message.from_user.id
    # TODO костыль убрать после проверки обновления создания юзера.
    tg_username = message.from_user.username
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
        error_text = (
            f"Ошибка при создании пользователя {tg_username}: ",
            f"{e}, вся инфа: {message.from_user}"
        )
        await send_message(
            SERVICE_CHAT_ID,
            error_text
        )
    # конец костыля
    application_storage.update_tg_id(tg_user_id)
    value = GET_PARAM_USER + str(tg_user_id)
    try:
        apllications_list = await get_apllications_list(message, value)
    except Exception as e:
        logging.info(f"Ошибка при получение спиcка заявок: {e}")
        await message.answer(MESSAGES["menu"], reply_markup=get_menu())

    if len(apllications_list) > 0:
        logging.info("Последняя заявка получена")
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
        await message.answer("Ваша последняя заявка была такой:")
        await print_apllication(message.answer)
        await message.answer(
            "Вы можете отредактировать заявку или отправить ее менеджеру:",
            reply_markup=get_application_fields_menu()
        )
    else:
        await message.answer("У вас еще нет заявок, создайте новую!")
        await message.answer(MESSAGES["menu"], reply_markup=get_menu())


@router.callback_query(lambda c: c.data == 'edit_cost')
async def get_new_cost(update: types.CallbackQuery, state: FSMContext):
    logging.info("Редактирование суммы заявки")
    await state.set_state(NewCost.edit_cost)
    await update.message.answer("Введите новую сумму заявки:")


@router.message(
    lambda message: message.text.isdigit(),
    NewCost.edit_cost
)
async def edit_cost(message: types.Message, state: FSMContext):
    application_cost = int(message.text)

    if application_cost < 100000:
        await message.answer("Сумма заявки должна быть от 100000!")
        await state.set_state(None)
        await message.answer(
            "Отредактируйте или отправьте заявку",
            reply_markup=get_application_fields_menu()
        )
        logging.info("Ошибка редактирования, сумма меньше 100000")
        return None

    logging.info("Сумма заявки отредактирована")
    application_storage.update_application_cost(application_cost)
    await message.answer(f"Вы ввели сумму заявки: {application_cost}")
    await print_apllication(message.answer)
    await state.set_state(None)
    await message.answer(
        "Отредактируйте или отправьте заявку",
        reply_markup=get_application_fields_menu()
    )


@router.message(F.text, NewCost.edit_cost)
async def invalid_values_application_cost(
    message: types.Message,
    state: FSMContext
):
    """Валидация сообщения с суммаой заявки."""
    logging.info("Ошибка редактирования суммы заявки")
    await message.answer(
        "Внимание! Сумма должна быть числом! Попробуйте еще раз.")


@router.callback_query(lambda c: c.data == 'edit_target_date')
async def get_new_target_data(update: types.CallbackQuery, state: FSMContext):
    logging.info("Редактирование даты")
    await state.set_state(NewTagetDate.edit_date)
    await update.message.answer(
        "Введите дату в формате: 20.10.25, не ранее текущего дня.",
        reply_markup=get_date_menu()
    )


# Обработка target_date step_4 (Кнопка)
@router.callback_query(
    lambda c: c.data in ["today", "tomorrow", "day_after_tomorrow"]
)
async def get_target_date_buttons(
    update: types.CallbackQuery,
    state: FSMContext
):
    logging.info("Дата заявки отредактирована")
    target_date = await get_date(update.data)
    application_storage.update_target_date(target_date)
    await update.message.answer(f"Вы ввели новую дату: {update.data}")
    await print_apllication(update.message.answer)
    await state.set_state(None)
    await update.message.answer(
        "Отредактируйте или отправьте заявку",
        reply_markup=get_application_fields_menu()
    )


# Обработка target_date step_4 (Сообщение)
@router.message(
    lambda message: validate_date(message.text),
    NewTagetDate.edit_date
)
async def edit_target_date(message: types.Message, state: FSMContext):
    logging.info("Дата заявки отредактирована")
    application_storage.update_target_date(message.text)
    await message.answer(f"Вы ввели новую дату: {message.text}")
    await print_apllication(message.answer)
    await state.set_state(None)
    await message.answer(
        "Отредактируйте или отправьте заявку",
        reply_markup=get_application_fields_menu()
    )


@router.message(F.text, NewTagetDate.edit_date)
async def invalid_values_target_date(
    message: types.Message,
    state: FSMContext
):
    """Валидация даты."""
    logging.info("Ошибка редактирования суммы заявки")
    await message.answer(
        "Вы ввели дату в неправильном формате!")
    await message.answer(
        "Введите дату в формате: 20.10.25, не ранее текущего дня."
    )


@router.callback_query(lambda c: c.data == 'edit_payer')
async def get_new_payer(update: types.CallbackQuery, state: FSMContext):
    logging.info("Редактирование плательщики начато")
    tg_user_id = update.from_user.id
    await state.set_state(NewPayer.edit_payer)
    await update.message.answer("Ваши компании плательщики:")
    company_list = await new_get_company_list(tg_user_id, EP_COMPANY_PAYER)
    if company_list:
        for company in company_list:
            company_text = MESSAGES["company"].format(
                company["company_name_payer"],
                company["company_inn_payer"]
            )
            await update.message.answer(
                company_text,
                reply_markup=get_company_inn_menu(company["company_inn_payer"])
            )
    global COMPANY_LIST_ALL
    COMPANY_LIST_ALL = company_list
    await update.message.answer(
        "Нажмите кнопку для выбора или введите новый ИНН!",
    )


@router.message(
    lambda message: message.text.isdigit() and len(message.text) == 10,
    NewPayer.edit_payer
)
@router.callback_query(
    lambda callback: callback.data.isdigit() and len(callback.data) == 10,
    NewPayer.edit_payer
)
async def process_inn_payer(
    update: types.Message | types.CallbackQuery,
    state: FSMContext
):
    """Редактирование сообщения с ИНН плательщика."""
    logging.info("Пользователь вводит нового плательщика")
    inn_payer = await extract_inn_from_update(update)
    answer_func = await get_answer_function(update)
    company_payer_storage.update_tg_id(update.from_user.id)

    if inn_payer in COMPANY_LIST_ALL:
        response = await get_company_by_inn(EP_COMPANY_PAYER, inn_payer)
        company_name = response["company_name_payer"]
        company_payer_storage.update_company_name(company_name)
        company_payer_storage.update_company_inn(inn_payer)
        await print_apllication(answer_func)
        await state.set_state(None)
        await answer_func(
            "Отредактируйте или отправьте заявку",
            reply_markup=get_application_fields_menu()
        )
    else:
        await answer_func(f"Вы ввели ИНН плательщика: {inn_payer}")
        company_payer_storage.update_company_inn(inn_payer)
        company_name = await get_company_name_from_dadata(
            inn_payer,
            answer_func
        )
        if company_name:
            await answer_func(f"Название вашей компании: {company_name}")
            company_payer_storage.update_company_name(company_name)
        await update_company_in_database(
            inn_payer,
            answer_func,
            EP_COMPANY_PAYER,
            company_payer_storage.to_dict(),
        )
        await print_apllication(answer_func)
        await state.set_state(None)
        await answer_func(
            "Отредактируйте или отправьте заявку",
            reply_markup=get_application_fields_menu()
        )


@router.message(F.text, NewPayer.edit_payer)
async def invalid_values_inn_payer(message: types.Message, state: FSMContext):
    """Валидация сообщения с числом из 10 символов."""
    logging.info("Ошибка ввода ИНН плательщика")
    await message.answer("Внимание! ИНН организации должен содержать 10 цифр!")
    await state.set_state(NewPayer.edit_payer)


@router.callback_query(lambda c: c.data == 'edit_recipient')
async def get_new_recipient(update: types.CallbackQuery, state: FSMContext):
    logging.info("Редактирование получателя начато")
    await state.set_state(NewRecipient.edit_recipient)
    await update.message.answer("Ваши компании получателя:")

    tg_user_id = update.from_user.id
    company_list = await new_get_company_list(tg_user_id, EP_COMPANY_RECIPIENT)
    if company_list:
        for company in company_list:
            company_text = MESSAGES["company"].format(
                company["company_name_recipient"],
                company["company_inn_recipient"]
            )
            await update.message.answer(
                company_text,
                reply_markup=get_company_inn_menu(
                    company["company_inn_recipient"]
                )
            )
    global COMPANY_LIST_ALL
    COMPANY_LIST_ALL = company_list
    await update.message.answer(
        "Нажмите кнопку для выбора или введите новый ИНН!"
    )


@router.message(
    lambda message: message.text.isdigit() and len(message.text) == 12,
    NewRecipient.edit_recipient
)
@router.callback_query(
    lambda callback: callback.data.isdigit() and len(callback.data) == 12,
    NewRecipient.edit_recipient
)
async def process_inn_recipient(
    update: types.Message | types.CallbackQuery,
    state: FSMContext
):
    """Редактирование сообщения с ИНН получателя."""
    logging.info("Пользователь вводит нового получателя")
    inn_recipient = await extract_inn_from_update(update)
    answer_func = await get_answer_function(update)
    company_recipient_storage.update_tg_id(update.from_user.id)

    if inn_recipient in COMPANY_LIST_ALL:
        response = await get_company_by_inn(
            EP_COMPANY_RECIPIENT, inn_recipient
        )
        company_name = response["company_name_recipient"]
        company_recipient_storage.update_company_name(company_name)
        company_recipient_storage.update_company_inn(inn_recipient)
        await print_apllication(answer_func)
        await state.set_state(None)
        await answer_func(
            "Отредактируйте или отправьте заявку",
            reply_markup=get_application_fields_menu()
        )
    else:
        await answer_func(f"Вы ввели ИНН получателя: {inn_recipient}")
        company_recipient_storage.update_company_inn(inn_recipient)
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
        await print_apllication(answer_func)
        await state.set_state(None)
        await answer_func(
            "Отредактируйте или отправьте заявку",
            reply_markup=get_application_fields_menu()
        )


@router.message(F.text, NewRecipient.edit_recipient)
async def invalid_values_inn_recipient(
    message: types.Message, state: FSMContext
):
    """Валидация сообщения с числом из 12 символов."""
    logging.info("Ошибка ввода ИНН плательщика")
    await message.answer("Внимание! ИНН организации должен содержать 12 цифр!")
    await state.set_state(NewRecipient.edit_recipient)


@router.callback_query(lambda c: c.data == 'send_apllication')
async def create_new_apllication(update: types.CallbackQuery):
    logging.info("Отправка заявки в БД")
    tg_username = update.from_user.username
    logging.info(f"Это tg_username: {tg_username}")

    data_dict = application_storage.to_dict()
    data_dict["inn_payer"] = company_payer_storage.company_inn
    data_dict["inn_recipient"] = company_recipient_storage.company_inn
    logging.info(f"Это data_dict: {data_dict}")

    try:
        response = await make_post_request(
            EP_APPLICATION, data_dict
        )
        data = json.loads(response.text)
        application_id = data["id"]
    except Exception as e:
        logging.info(f"Ошибка при создании заявки: {e}")
        await send_message(
            SERVICE_CHAT_ID, f"Ошибка создания повторной заявки {e}")
        await update.message.answer(TECH_MESSAGES["api_error"])
        await update.message.answer(MESSAGES["menu"], reply_markup=get_menu())
        logging.info(f"Пользователь {tg_username} в меню")

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
            update.from_user.first_name,
            tg_username,
            application_message
        )
        message_user = MESSAGES["application_created"].format(
            application_message
        )
        await send_message(SERVICE_CHAT_ID, message_manager)
        await send_message(MANAGER_CHAT_ID, message_manager)

        await update.message.answer(message_user)

    application_storage.clear_data()
    company_payer_storage.clear_data()
    company_recipient_storage.clear_data()
    await update.message.answer(MESSAGES["menu"], reply_markup=get_menu())
    logging.info(f"Пользователь {tg_username} в меню")
