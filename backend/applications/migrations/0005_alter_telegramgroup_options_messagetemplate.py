# Generated by Django 5.0.6 on 2024-12-07 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("applications", "0004_telegramgroup"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="telegramgroup",
            options={
                "verbose_name": "Группа для рассылок в tg",
                "verbose_name_plural": "Группы для рассылок в tg",
            },
        ),
        migrations.CreateModel(
            name="MessageTemplate",
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
                ("title", models.CharField(max_length=255)),
                ("content", models.TextField()),
                (
                    "groups",
                    models.ManyToManyField(
                        related_name="message_templates",
                        to="applications.telegramgroup",
                    ),
                ),
            ],
        ),
    ]
