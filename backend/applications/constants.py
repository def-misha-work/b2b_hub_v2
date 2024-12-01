import os

from dotenv import load_dotenv

load_dotenv()

TG_DOMAIN = "https://api.telegram.org/"
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT = "bot"
URL_TG_SEND_MESSAGE = TG_DOMAIN + BOT + BOT_TOKEN + "/sendMessage"
URL_SEND_FILE = TG_DOMAIN + BOT + BOT_TOKEN + "/sendDocument"
VALID_STATUSES = ["Новая", "В работе", "Счёт в оплате", "Выполнена"]


NEW_STATUS_MESSAGE = """
B2b-hub: изменился статус вашей заявки.

Статус заявки: {},
Номер заявки: {},
Сумма заявки: {},
Дата выполнения заявки: {}
"""


NEW_DOC_MESSAGE = """
B2b-hub: новый документ по вашей заявке номер: {}
{}
"""
UPDATE_DOC_MESSAGE = """
B2b-hub: <b>ВНИМАНИЕ</b>, обновился документ по заявке номер: {}
{}
"""
