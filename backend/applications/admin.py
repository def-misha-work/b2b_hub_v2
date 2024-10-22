import logging
import requests

from django.contrib import admin, messages
from requests.exceptions import RequestException

from applications.models import (
    TelegamUsers,
    CompaniesPayer,
    CompaniesRecipient,
    Applications,
)
from applications.constants import (
    URL_TG_SEND_MESSAGE,
    NEW_STATUS_MESSAGE
)


class TelegamUsersAdmin(admin.ModelAdmin):
    list_display = (
        "tg_user_id",
        "tg_username",
        "name",
        "lastname",
    )


class CompaniesPayerAdmin(admin.ModelAdmin):
    list_display = (
        "tg_user",
        "company_name_payer",
        "company_inn_payer",
    )


class CompaniesRecipientAdmin(admin.ModelAdmin):
    list_display = (
        "tg_user",
        "company_name_recipient",
        "company_inn_recipient",
    )


class ApplicationsAdmin(admin.ModelAdmin):
    fields = (
        "app_status",
        "created_at",
        "updated_at",
        "tg_user",
        "cost",
        "target_date",
        "inn_payer",
        "inn_recipient",
    )
    readonly_fields = ("created_at", "updated_at")
    list_display = (
        "app_status",
        "id",
        "created_at",
        "tg_user",
        "cost",
        "target_date",
        "inn_payer",
        "inn_recipient",
    )
    list_filter = (
        "created_at",
        "app_status",
    )
    search_fields = (
        "id",
        "cost",
        "tg_user__tg_username",
        "tg_user__name",
        "tg_user__lastname",
        "inn_payer__company_name_payer",
        "inn_payer__company_inn_payer",
        "inn_recipient__company_name_recipient",
        "inn_recipient__company_inn_recipient",
    )
    ordering = ("created_at",)

    def save_model(self, request, instance, form, change):
        old_app_status = None
        if change:
            old_app_status = Applications.objects.get(
                pk=instance.pk
            ).app_status
        super().save_model(request, instance, form, change)

        if old_app_status != instance.app_status:
            text = NEW_STATUS_MESSAGE.format(
                instance.app_status,
                instance.id,
                instance.cost,
                instance.target_date,
            )
            params = {
                "chat_id": instance.tg_user.tg_user_id,
                "text": text
                }
            try:
                response = requests.get(URL_TG_SEND_MESSAGE, params)
                response.raise_for_status()
            except RequestException as e:
                logging.error(f"Ошибка при отправке запроса: {e}")
                messages.error(request, f"Ошибка при отправке запроса: {e}")
                return None


admin.site.register(TelegamUsers, TelegamUsersAdmin)
admin.site.register(CompaniesPayer, CompaniesPayerAdmin)
admin.site.register(CompaniesRecipient, CompaniesRecipientAdmin)
admin.site.register(Applications, ApplicationsAdmin)
