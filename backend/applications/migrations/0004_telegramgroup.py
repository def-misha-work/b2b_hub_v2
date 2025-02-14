# Generated by Django 5.0.6 on 2024-12-07 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("applications", "0003_applications_app_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="TelegramGroup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=255, unique=True, verbose_name="Название группы"
                    ),
                ),
                (
                    "users",
                    models.ManyToManyField(
                        related_name="groups",
                        to="applications.telegamusers",
                        verbose_name="Пользователи",
                    ),
                ),
            ],
            options={
                "verbose_name": "Группа пользователей",
                "verbose_name_plural": "Группы пользователей",
            },
        ),
    ]
