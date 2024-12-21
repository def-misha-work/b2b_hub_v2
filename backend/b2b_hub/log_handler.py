import os
import logging


class RotatingFileHandler(logging.FileHandler):
    def __init__(
        self,
        filename,
        max_bytes=100 * 1024 * 1024,
        backup_count=1,
        *args,
        **kwargs
    ):
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.filename = filename
        super().__init__(filename, *args, **kwargs)

    def emit(self, record):
        if os.path.exists(
            self.filename
        ) and os.path.getsize(self.filename) > self.max_bytes:
            self.rotate()
        super().emit(record)

    def rotate(self):
        if os.path.exists(self.filename):
            # Переименовываем текущий файл
            new_filename = 'old_' + os.path.basename(self.filename)
            os.rename(self.filename, new_filename)
            # Создаем новый файл для записи логов
            self.stream = self._open()  # Открываем новый файл для записи


def get_rotating_file_handler():
    return RotatingFileHandler('django_app.log')
