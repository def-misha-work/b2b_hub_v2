import os

from dotenv import load_dotenv

load_dotenv()

TG_DOMAIN = "https://api.telegram.org/"
BOT_TOKEN = os.getenv("BOT_TOKEN")
URL_TG_BOT_ALERT = TG_DOMAIN + "bot" + BOT_TOKEN + "/sendMessage"
VALID_STATUSES = ["Новая", "В работе", "Счёт в оплате", "Выполнена"]


APPLICATION_MESSAGE = """
Уведомление, поменялся статус заявки!

Статус заявки: {},
Номер заявки: {},
Сумма заявки: {},
Дата выполнения заявки: {}
"""

# APPLICATION_MESSAGE = """
# Статус заявки: {},
# Номер заявки: {},
# Сумма заявки: {},
# Дата выполнения заявки: {}
# Плательщик: {},
# ИНН плательщика: {},
# Получатель: {},
# ИНН получателя: {},
# """
