from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication

from applications.serializers import (
    TelegamUsersSerializer,
    CompaniesPayerSerializer,
    CompaniesRecipientSerializer,
    ApplicationsSerializer,
    ApplicationsPostUpdateSerializer,
)
from applications.models import (
    Applications,
    CompaniesPayer,
    CompaniesRecipient,
    TelegamUsers,
)


class TelegamUsersViewSet(viewsets.ModelViewSet):
    queryset = TelegamUsers.objects.all().order_by("created_at")
    serializer_class = TelegamUsersSerializer
    authentication_classes = [BasicAuthentication]
    lookup_field = 'tg_user_id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CompaniesPayerViewSet(viewsets.ModelViewSet):
    queryset = CompaniesPayer.objects.all().order_by("created_at")
    serializer_class = CompaniesPayerSerializer
    authentication_classes = [BasicAuthentication]
    lookup_field = 'company_inn'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CompaniesRecipientViewSet(viewsets.ModelViewSet):
    queryset = CompaniesRecipient.objects.all().order_by("created_at")
    serializer_class = CompaniesRecipientSerializer
    authentication_classes = [BasicAuthentication]
    lookup_field = 'company_inn'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ApplicationsViewSet(viewsets.ModelViewSet):
    queryset = Applications.objects.all().order_by("created_at")
    serializer_class = ApplicationsSerializer
    authentication_classes = [BasicAuthentication]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ApplicationsSerializer
        return ApplicationsPostUpdateSerializer
