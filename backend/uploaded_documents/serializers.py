from rest_framework import serializers
from uploaded_documents.models import UploadedFile


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = (
            "tg_user_id",
            "app_id",
            "json_data",
        )
