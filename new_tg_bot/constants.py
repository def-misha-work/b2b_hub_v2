import os

from dotenv import load_dotenv

load_dotenv()

# Подключение бота
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
DOMANE_NAME = os.getenv("DOMANE_NAME")

# Авторизация в беке
BASIC_USER_LOGIN = os.getenv("BASIC_USER_LOGIN")
BASIC_USER_PASSWORD = os.getenv("BASIC_USER_PASSWORD")


# Собщения
START_MESSAGE = "Добрый день, {}!\nСервис B2Bhub приветствует Вас!"
NO_USER_NAME = (
    """Для начала работы с ботом требуется"""
    """указать Ваше имя, напишите его, пожалуйста!"""
)
MAIN_MENU_MESSAGE = "Вы в меню!"
INPUT_INN_PAYER_MESSAGE = (
    """Шаг 1 из 4:\n"""
    """Создание новой заявки:\n"""
    """Укажите ИНН вашей организации, кто будет плательщиком."""
)
