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
        file_obj = request.FILES.get("file")
        tg_user_id = request.data.get("tg_user_id")
        app_id = request.data.get("app_id")

        if not tg_user_id or not app_id:
            return Response(
                {"error": "No field tg_user_id or app_id"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not file_obj:
            return Response(
                {"error": "No file"},
                status=status.HTTP_400_BAD_REQUEST
            )

        params = {
            "chat_id": tg_user_id,
            "text": NEW_DOC_MESSAGE.format(app_id, file_obj.name)
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

        url = URL_SEND_FILE + f"?chat_id={tg_user_id}"
        files = {"document": (file_obj.name, file_obj.read())}

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

        return Response(
            {"message": "File uploaded successfully"},
            status=status.HTTP_200_OK
        )
