from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication

from applications.serializers import (
    TelegamUsersSerializer,
    CompaniesPayerSerializer,
    CompaniesRecipientSerializer,
    ApplicationsSerializer,
)
from applications.models import (
    Applications,
    CompaniesPayer,
    CompaniesRecipient,
    TelegamUsers,
)


class TelegamUsersViewSet(viewsets.ModelViewSet):
    queryset = TelegamUsers.objects.all().order_by("id")
    serializer_class = TelegamUsersSerializer
    authentication_classes = [BasicAuthentication]


class CompaniesPayerViewSet(viewsets.ModelViewSet):
    queryset = CompaniesPayer.objects.all().order_by("id")
    serializer_class = CompaniesPayerSerializer
    authentication_classes = [BasicAuthentication]


class CompaniesRecipientViewSet(viewsets.ModelViewSet):
    queryset = CompaniesRecipient.objects.all().order_by("id")
    serializer_class = CompaniesRecipientSerializer
    authentication_classes = [BasicAuthentication]


class ApplicationsViewSet(viewsets.ModelViewSet):
    queryset = Applications.objects.all().order_by("id")
    serializer_class = ApplicationsSerializer
    authentication_classes = [BasicAuthentication]
