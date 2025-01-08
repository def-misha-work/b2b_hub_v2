import os
import base64
import requests
import json

from rest_framework import viewsets, status
from rest_framework.response import Response

from uploaded_documents.serializers import UploadedFileSerializer
from applications.constants import (
    NEW_DOC_MESSAGE,
    UPDATE_DOC_MESSAGE,
    REQUIRED_FIELDS,
)

from uploaded_documents.utils import (
    send_file,
    send_message,
)


class UploadFileViewSet(viewsets.ViewSet):
    def create(self, request):
        if any(request.data.get(field) is None for field in REQUIRED_FIELDS):
            return Response(
                {"error": "Missing fields"},
                status=status.HTTP_400_BAD_REQUEST
            )
        tg_user_id = request.data.get("tg_user_id")
        app_id = request.data.get("app_id")
        file_body = request.data.get("file_body")
        file_name = request.data.get("file_name")
        message = request.data.get("message")
        json_data = request.data

        serializer = UploadedFileSerializer(data={
            "tg_user_id": tg_user_id,
            "app_id": app_id,
            "json_data": json.dumps(json_data),
        })

        if serializer.is_valid():
            uploaded_file_instance = serializer.save()
        else:
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        # определяем какое сообщение отправляем
        text = UPDATE_DOC_MESSAGE if message == "update" else NEW_DOC_MESSAGE

        # Отправляем сообщение
        try:
            send_message(tg_user_id, text.format(app_id, file_name))
            uploaded_file_instance.dispatch_status = 200
        except requests.HTTPError as e:
            uploaded_file_instance.dispatch_status = str(e)
            uploaded_file_instance.save()
            return Response(
                {"error": f"Failed to send message: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # отправляем файл
        file_data = base64.b64decode(file_body)
        with open(file_name, 'wb') as temp_file:
            temp_file.write(file_data)

        try:
            send_file(tg_user_id, file_name)
            uploaded_file_instance.dispatch_status = 200
        except requests.RequestException as e:
            uploaded_file_instance.dispatch_status = str(e)
            uploaded_file_instance.save()
            return Response(
                {"error": f"Failed to upload file: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Удаляем временно созданный файл
        os.remove(file_name)
        uploaded_file_instance.save()
        return Response(
            {"message": "File uploaded successfully"},
            status=status.HTTP_200_OK
        )
