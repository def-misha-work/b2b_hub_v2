# Generated by Django 5.0.6 on 2024-07-12 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("applications", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="telegamusers",
            name="tg_user_id",
            field=models.TextField(unique=True, verbose_name="ID автора заявки в tg"),
        ),
    ]
