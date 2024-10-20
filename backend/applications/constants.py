import os

from dotenv import load_dotenv

load_dotenv()

TG_DOMAIN = "https://api.telegram.org/"
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT = "bot"
URL_TG_BOT_ALERT = TG_DOMAIN + BOT + BOT_TOKEN + "/sendMessage"
URL_SEND_FILE = TG_DOMAIN + BOT + BOT_TOKEN + "/sendDocument"
VALID_STATUSES = ["Новая", "В работе", "Счёт в оплате", "Выполнена"]


APPLICATION_MESSAGE = """
B2b-hub: изменился статус вашей заявки.

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
