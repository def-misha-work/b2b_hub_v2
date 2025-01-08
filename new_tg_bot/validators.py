from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def validate_date(date_str):
    # Список форматов даты, которые мы поддерживаем
    date_formats = ['%d.%m.%y', '%d.%m.%Y']

    for date_format in date_formats:
        try:
            # Пытаемся преобразовать строку в дату
            date = datetime.strptime(date_str, date_format)
            # Проверяем, что дата строго в будущем
            if date.date() >= datetime.now().date():
                return True
            else:
                logger.error(f"Дата {date_str} находится в прошлом")
                return False
        except ValueError:
            continue  # Пробуем следующий формат

    # Если ни один формат не подошел
    logger.error(f"Неправильный формат даты: {date_str}")
    return False
