import requests

from applications.constants import (
    URL_TG_SEND_MESSAGE,
    URL_SEND_FILE,
)


def send_message(tg_user_id, text):
    params = {
        "chat_id": tg_user_id,
        "text": text,
        "parse_mode": "HTML"
    }
    response = requests.get(URL_TG_SEND_MESSAGE, params)
    response.raise_for_status()
    return response


def send_file(tg_user_id, file_name):
    with open(file_name, 'rb') as file_to_send:
        url = URL_SEND_FILE + f"?chat_id={tg_user_id}"
        files = {'document': file_to_send}
        response = requests.post(url, files=files)
        response.raise_for_status()
        return response
