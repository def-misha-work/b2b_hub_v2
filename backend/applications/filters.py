import django_filters
from applications.models import Applications


class ApplicationsFilter(django_filters.FilterSet):
    app_status = django_filters.CharFilter(
        field_name="app_status", lookup_expr="exact"
    )

    class Meta:
        model = Applications
        fields = ["app_status"]
