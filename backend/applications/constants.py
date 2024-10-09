import os

from dotenv import load_dotenv

load_dotenv()

TG_DOMAIN = "https://api.telegram.org/bot"
BOT_TOKEN = os.getenv("BOT_TOKEN")
URL_TG_BOT_ALERT = TG_DOMAIN + BOT_TOKEN + "/sendMessage"
VALID_STATUSES = ["Новая", "В работе", "Счёт в оплате", "Выполнена"]
