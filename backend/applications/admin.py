from django.contrib import admin

from applications.models import (
    TelegamUsers,
    CompaniesPayer,
    CompaniesRecipient,
    Applications,
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
        "created_at",
        "updated_at",
        "tg_user",
        "cost",
        "target_date",
        "inn_payer",
        "inn_recipient",
        "app_status",
    )
    readonly_fields = ("created_at", "updated_at")
    list_display = (
        "id",
        "created_at",
        "tg_user",
        "cost",
        "target_date",
        "inn_payer",
        "inn_recipient",
        "app_status",
    )
    list_filter = (
        "created_at",
        "tg_user",
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


admin.site.register(TelegamUsers, TelegamUsersAdmin)
admin.site.register(CompaniesPayer, CompaniesPayerAdmin)
admin.site.register(CompaniesRecipient, CompaniesRecipientAdmin)
admin.site.register(Applications, ApplicationsAdmin)
