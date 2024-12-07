import logging
import requests

from django.contrib import admin, messages
from requests.exceptions import RequestException

from applications.models import (
    TelegamUsers,
    CompaniesPayer,
    CompaniesRecipient,
    Applications,
    TelegramGroup,
    MessageTemplate,
)
from applications.constants import (
    URL_TG_SEND_MESSAGE,
    NEW_STATUS_MESSAGE
)
from applications.utils import (
    send_message_to_group
)


# class CustomAdminSite(admin.AdminSite):
#     def get_app_list(self, request):
#         """
#         Return a sorted list of all the installed apps that have been
#         registered in this site.
#         """
#         app_dict = self._build_app_dict(request)
#         app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

#         # Customize the order of models within each app
#         for app in app_list:
#             if app['app_label'] == 'applications':
#                 app['models'].sort(key=lambda x: {
#                     'Applications': 1,
#                     'CompaniesRecipient': 2,
#                     'CompaniesPayer': 3,
#                     'TelegamUsers': 4,
#                     'TelegramGroup': 5,
#                     'MessageTemplate': 6,
#                 }.get(x['object_name'], 999))

#         return app_list


# custom_admin_site = CustomAdminSite(name='custom_admin')


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


class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = ('title',)
    filter_horizontal = ('groups',)

    def send_message(self, request, queryset):
        for template in queryset:
            for group in template.groups.all():
                send_message_to_group(group.id, template.content)
        self.message_user(request, "Сообщения отправлены.")

    send_message.short_description = "Отправить сообщение выбранным шаблонам"

    actions = [send_message]


class TelegramGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('users',)


admin.site.register(MessageTemplate, MessageTemplateAdmin)
admin.site.register(TelegramGroup, TelegramGroupAdmin)
admin.site.register(TelegamUsers, TelegamUsersAdmin)
admin.site.register(CompaniesPayer, CompaniesPayerAdmin)
admin.site.register(CompaniesRecipient, CompaniesRecipientAdmin)
admin.site.register(Applications, ApplicationsAdmin)

# custom_admin_site.register(TelegramGroup, TelegramGroupAdmin)
# custom_admin_site.register(TelegamUsers, TelegamUsersAdmin)
# custom_admin_site.register(CompaniesPayer, CompaniesPayerAdmin)
# custom_admin_site.register(CompaniesRecipient, CompaniesRecipientAdmin)
# custom_admin_site.register(Applications, ApplicationsAdmin)
# custom_admin_site.register(MessageTemplate, MessageTemplateAdmin)
