from django.contrib import admin
from uploaded_documents.models import UploadedFile


class UploadedFileAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "tg_user_id",
        "app_id",
        "dispatch_status",
    )


admin.site.register(UploadedFile, UploadedFileAdmin)
