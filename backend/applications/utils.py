import requests

from applications.constants import URL_TG_SEND_MESSAGE
from applications.models import TelegramGroup


def send_message_to_user(chat_id, message):
    url = URL_TG_SEND_MESSAGE
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML',
    }
    response = requests.post(url, json=payload)
    return response.json()


def send_message_to_group(group_id, message):
    group = TelegramGroup.objects.get(id=group_id)
    for user in group.users.all():
        send_message_to_user(user.tg_user_id, message)
