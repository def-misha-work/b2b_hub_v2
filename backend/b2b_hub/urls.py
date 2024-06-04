from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import routers, permissions

from applications.views import (
    TelegamUsersViewSet,
    CompaniesPayerViewSet,
    CompaniesRecipientViewSet,
    ApplicationsViewSet
)

router = routers.DefaultRouter()
router.register(r"tg_users", TelegamUsersViewSet, basename='tg_user')
router.register(
    r"companies_payer",
    CompaniesPayerViewSet,
    basename='companies_payer'
)
router.register(
    r"companies_recipient",
    CompaniesRecipientViewSet,
    basename='companies_recipient'
)
router.register(r"applications", ApplicationsViewSet, basename='applications')

schema_view = get_schema_view(
    openapi.Info(
        title="B2B API",
        default_version="v1",
        description="API для телеграмм бота b2b hub",
    ),
    # patterns=[
    #     path("api/v1/", include(router.urls)),
    # ],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    re_path(
        r"^api/v1/docs/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
