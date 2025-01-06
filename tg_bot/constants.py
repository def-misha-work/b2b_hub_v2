import os

from dotenv import load_dotenv

load_dotenv()

# Подключение бота
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
SERVICE_TELEGRAM_TOKEN = os.getenv("SERVICE_TELEGRAM_TOKEN")
SERVICE_CHAT_ID = os.getenv("SERVICE_CHAT_ID")
MANAGER_CHAT_ID = os.getenv("MANAGER_CHAT_ID")
DOMANE_NAME = os.getenv("DOMANE_NAME")

# Работа с эндпоинтами джанго
ENDPONT_CREATE_USER = DOMANE_NAME + "api/v1/tg_users/"
# Payer
EP_COMPANY_PAYER = DOMANE_NAME + "api/v1/companies_payer/"
# Recipient
EP_COMPANY_RECIPIENT = DOMANE_NAME + "api/v1/companies_recipient/"
# Apllications
EP_APPLICATION = DOMANE_NAME + "api/v1/applications/"
GET_PARAM_USER = "?tg_user__tg_user_id="
# Получение информации о компании по ИНН
ENDPONT_GET_COMPANY_NAME = "http://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party" # noqa
DADATA_API_KEY = os.getenv("DADATA_API_KEY")

BASIC_USER_LOGIN = os.getenv("BASIC_USER_LOGIN")
BASIC_USER_PASSWORD = os.getenv("BASIC_USER_PASSWORD")

start_message = "Добрый день, {}!\nСервис B2Bhub приветствует Вас!"
menu_message = "Это Меню, выберите что Вы хотите сделать:"
step1_message = """
Шаг 1 из 4:
\nСоздание новой заявки:
\nУкажите ИНН вашей организации, кто будет плательщиком.
"""
step2_message = "Шаг 2 из 4:\nУкажите ИНН вашего ИП, кто будет получателем."
step3_message = """
Шаг 3 из 4:
\nВведите сумму заявки в рублях без указания валюты и без пробелов.
\nНапример: 100000 или 1000000.
"""
step4_message = """
Шаг 4 из 4:
\nВведите дату к которой заявку нужно выполнить, в формате: дд.мм.гг.
\nНапример: 20.10.25 или 20.10.2025
\nЛибо воспользуйтесь кнопками.
"""
application_message = """
Номер заявки: {},
Сумма заявки: {},
Желаемая дата исполнения: {}
Плательщик: {},
ИНН плательщика: {},
Получатель: {},
ИНН получателя: {},
"""

application_repeat = """
Сумма заявки: {},
Желаемая дата исполнения: {}
Плательщик: {},
ИНН плательщика: {},
Получатель: {},
ИНН получателя: {},
"""

application_created_message = """
Ваша заявка создана: {}
Мы свяжемся в Вами в ближайшее рабочее время. Спасибо!
"""
company_message = "Название компании: {}\nИНН компании: {}"


MESSAGES = {
    "start": start_message,
    "menu": menu_message,
    "step1": step1_message,
    "step2": step2_message,
    "step3": step3_message,
    "step4": step4_message,
    "application": application_message,
    "application_created": application_created_message,
    "company": company_message,
    "application_repeat": application_repeat,
}

MESSAGES_TO_MANAGER = {
    "application_created": (
        "Заявка от пользователя: {},\n"
        "Ник в TG: @{}\n"
        "Заявка: {}"
    ),
}

TECH_MESSAGES = {
    "alert_message": "Извините, но я могу обработать только текст",
    "api_error": (
        "Извините, произошла ошибка, попробуйте еще раз через пару минут. "
        "Администратор уже получил уведомление о ошибке."
    ),
    "company_error": "Не удалось получить названия компании по ИНН",
}

CASH = "ИП Наличкин Александр Иванович"
