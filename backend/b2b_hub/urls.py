from django.contrib import admin
from django.urls import include, path


# router = routers.DefaultRouter()


urlpatterns = [
    path("admin/", admin.site.urls),
    # path('api/', include(router.urls)),
]
