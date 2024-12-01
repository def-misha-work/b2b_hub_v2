import os
import base64
import requests

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication

from applications.serializers import (
    TelegamUsersSerializer,
    CompaniesPayerSerializer,
    CompaniesPostUpdatePayerSerializer,
    CompaniesRecipientSerializer,
    CompaniesPostUpdateRecipientSerializer,
    ApplicationsSerializer,
    ApplicationsPostUpdateSerializer,
)
from applications.models import (
    Applications,
    CompaniesPayer,
    CompaniesRecipient,
    TelegamUsers,
)
from applications.constants import (
    URL_TG_SEND_MESSAGE,
    URL_SEND_FILE,
    NEW_DOC_MESSAGE,
    UPDATE_DOC_MESSAGE,
)


class TelegamUsersViewSet(viewsets.ModelViewSet):
    queryset = TelegamUsers.objects.all().order_by("created_at")
    serializer_class = TelegamUsersSerializer
    authentication_classes = [BasicAuthentication]
    lookup_field = "tg_user_id"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Проверет, существует ли объект с таким tg_user_id."""
        tg_user_id = request.data.get("tg_user_id")
        if TelegamUsers.objects.filter(tg_user_id=tg_user_id).exists():
            instance = TelegamUsers.objects.get(tg_user_id=tg_user_id)
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return super().create(request, *args, **kwargs)


class CompaniesPayerViewSet(viewsets.ModelViewSet):
    queryset = CompaniesPayer.objects.all().order_by("created_at")
    serializer_class = CompaniesPayerSerializer
    authentication_classes = [BasicAuthentication]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ["tg_user__tg_user_id"]
    lookup_field = "company_inn_payer"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CompaniesPayerSerializer
        return CompaniesPostUpdatePayerSerializer

    def create(self, request, *args, **kwargs):
        """Проверет, существует ли объект с таким company_inn_payer."""
        company_inn_payer = request.data.get("company_inn_payer")
        if CompaniesPayer.objects.filter(
            company_inn_payer=company_inn_payer
        ).exists():
            instance = CompaniesPayer.objects.get(
                company_inn_payer=company_inn_payer
            )
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return super().create(request, *args, **kwargs)


class CompaniesRecipientViewSet(viewsets.ModelViewSet):
    queryset = CompaniesRecipient.objects.all().order_by("created_at")
    serializer_class = CompaniesRecipientSerializer
    authentication_classes = [BasicAuthentication]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ["tg_user__tg_user_id"]
    lookup_field = "company_inn_recipient"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CompaniesRecipientSerializer
        return CompaniesPostUpdateRecipientSerializer

    def create(self, request, *args, **kwargs):
        """Проверяет, существует ли объект с таким company_inn_recipient."""
        company_inn_recipient = request.data.get("company_inn_recipient")
        if CompaniesRecipient.objects.filter(
            company_inn_recipient=company_inn_recipient
        ).exists():
            instance = CompaniesRecipient.objects.get(
                company_inn_recipient=company_inn_recipient
            )
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return super().create(request, *args, **kwargs)


class ApplicationsViewSet(viewsets.ModelViewSet):
    queryset = Applications.objects.all().order_by("created_at")
    serializer_class = ApplicationsSerializer
    authentication_classes = [BasicAuthentication]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ["tg_user__tg_user_id"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ApplicationsSerializer
        return ApplicationsPostUpdateSerializer


class UploadFileViewSet(viewsets.ViewSet):
    def create(self, request):
        tg_user_id = request.data.get("tg_user_id")
        app_id = request.data.get("app_id")
        file_body = request.data.get("file_body")
        file_name = request.data.get("file_name")
        message = request.data.get("message")

        if not all([tg_user_id, app_id, file_body, file_name, message]):
            return Response(
                {"error": "No any fields"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # определяем какое сообщение отправляем
        if message == "update":
            text = UPDATE_DOC_MESSAGE
        else:
            text = NEW_DOC_MESSAGE
        # Отправляем сообщение
        params = {
            "chat_id": tg_user_id,
            "text": text.format(app_id, file_name),
            "parse_mode": "HTML"
        }
        try:
            response = requests.get(URL_TG_SEND_MESSAGE, params)
            response.raise_for_status()
        except requests.HTTPError as e:
            return Response(
                {"error": f"Failed to send message: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except requests.RequestException as e:
            return Response(
                {"error": f"Network error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        # отправляем файл
        file_data = base64.b64decode(file_body)
        with open(file_name, 'wb') as temp_file:
            temp_file.write(file_data)

        with open(file_name, 'rb') as file_to_send:
            url = URL_SEND_FILE + f"?chat_id={tg_user_id}"
            files = {'document': file_to_send}
            try:
                response = requests.post(url, files=files)
                response.raise_for_status()
            except requests.HTTPError as e:
                return Response(
                    {"error": f"Failed to upload file: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except requests.RequestException as e:
                return Response(
                    {"error": f"Network error: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        # удаляем временно созданый файл
        os.remove(file_name)
        return Response(
            {"message": "File uploaded successfully"},
            status=status.HTTP_200_OK
        )
