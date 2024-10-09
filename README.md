# b2b_hub_v2

### Запуск бекэнда ###
Создание вирт окружения
```bash
python3 -m venv .venv
```

Активация вирт окружения
```bash
source .venv/bin/activate
```

Абгрейд pip
```bash
python -m pip install --upgrade pip
```

Установка зависимостей
```bash
pip install -r requirements.txt
```

### Запуск бота ###

Создание вирт окружения
```bash
python3 -m venv .venv
```

Активация вирт окружения
```bash
source .venv/bin/activate
```

Абгрейд pip
```bash
python -m pip install --upgrade pip
```

Установка зависимостей
```bash
pip install -r requirements.txt
```

```bash
python bot.py
```

### Для переключения между версиями разаботки и прода###
В tg_bot
1) В .env расскоментировать соответствющие константы
TELEGRAM_TOKEN
SERVICE_TELEGRAM_TOKEN
MANAGER_CHAT_ID
2) В .env поменять юзера джанги для авторизации
BASIC_USER_LOGIN=1@1.ru
BASIC_USER_PASSWORD=1
3) В constants.py поменять DOMANE_NAME на локальную или прод версию.
