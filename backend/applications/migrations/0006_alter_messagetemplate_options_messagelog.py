# Generated by Django 5.0.6 on 2024-12-07 17:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("applications", "0005_alter_telegramgroup_options_messagetemplate"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="messagetemplate",
            options={
                "verbose_name": "Шаблоны для отправки в tg",
                "verbose_name_plural": "Шаблоны для отправки в tg",
            },
        ),
        migrations.CreateModel(
            name="MessageLog",
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
                ("status_code", models.IntegerField()),
                ("success", models.BooleanField(default=False)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="logs",
                        to="applications.telegramgroup",
                    ),
                ),
                (
                    "template",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="logs",
                        to="applications.messagetemplate",
                    ),
                ),
            ],
        ),
    ]
