from django_filters import rest_framework as filters

from dealership.models import Dealership, Brand, Model, Car


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class DealershipFilter(filters.FilterSet):
    name = CharFilterInFilter(field_name="name", lookup_expr="in")
    brand = CharFilterInFilter(field_name="brand__name", lookup_expr="in")
    location = CharFilterInFilter(field_name="location", lookup_expr="in")
    balance = filters.NumberFilter(field_name="balance")
    contact_number = CharFilterInFilter(
        field_name="contact_number", lookup_expr="in")

    class Meta:
        model = Dealership
        fields = ["name", "brand", "location", "balance", "contact_number"]


class BrandFilter(filters.FilterSet):
    name = CharFilterInFilter(field_name="name", lookup_expr="in")

    class Meta:
        model = Brand
        fields = ["name"]


class ModelFilter(filters.FilterSet):
    name = CharFilterInFilter(field_name="name", lookup_expr="in")
    brand = CharFilterInFilter(field_name="brand__name", lookup_expr="in")
    drivetrain = CharFilterInFilter(field_name="drivetrain", lookup_expr="in")
    engine = CharFilterInFilter(field_name="engine", lookup_expr="in")
    bodytype = CharFilterInFilter(field_name="bodytype", lookup_expr="in")
    transmission = CharFilterInFilter(
        field_name="transmission", lookup_expr="in")

    class Meta:
        model = Model
        fields = [
            "name",
            "brand",
            "drivetrain",
            "engine",
            "bodytype",
            "transmission"]


class CarFilter(filters.FilterSet):
    name = CharFilterInFilter(field_name="name", lookup_expr="in")
    model = CharFilterInFilter(field_name="model__name", lookup_expr="in")
    price = CharFilterInFilter(field_name="model__name", lookup_expr="in")

    class Meta:
        model = Car
        fields = ["name", "model", "price"]
