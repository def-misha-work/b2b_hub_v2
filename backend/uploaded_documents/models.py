from django.db import models

from applications.models import (
    TimestampMixin,
)


class UploadedFile(TimestampMixin, models.Model):
    tg_user_id = models.CharField(max_length=255)
    app_id = models.CharField(max_length=255)
    json_data = models.TextField()
    dispatch_status = models.CharField(
        max_length=50,
        default="received",
        )

    def __str__(self):
        return f"Файл от юзера {self.tg_user_id} по заявке {self.app_id}"
