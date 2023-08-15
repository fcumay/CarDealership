from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model

User = get_user_model()


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class UserFilter(filters.FilterSet):
    name = CharFilterInFilter(field_name="name", lookup_expr="in")

    class Meta:
        model = User
        fields = ["name"]
