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
    return response


def send_message_to_group(group_id, message):
    group = TelegramGroup.objects.get(id=group_id)
    arguments = [(user.tg_user_id, message) for user in group.users.all()]
    return arguments
