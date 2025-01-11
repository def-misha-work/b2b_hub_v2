import os

from dotenv import load_dotenv

load_dotenv()

# Подключение бота
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


# Собщения
START_MESSAGE = "Добрый день, {}!\nСервис B2Bhub приветствует Вас!"
NO_USER_NAME = (
    """Для начала работы с ботом требуется"""
    """указать Ваше имя, напишите его, пожалуйста!"""
)
