from django_filters import rest_framework as filters

from dealer.models import Dealer, DealerInventory, BuyingHistoryDealer, PromotionDealership, PromotionDealer


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class DealerFilter(filters.FilterSet):
    name = CharFilterInFilter(field_name="name", lookup_expr="in")
    location = CharFilterInFilter(field_name="location", lookup_expr="in")
    amount_of_client = filters.NumberFilter(field_name="amount_of_client")
    contact_number = CharFilterInFilter(
        field_name="contact_number", lookup_expr="in")

    class Meta:
        model = Dealer
        fields = ["name", "location", "amount_of_client", "contact_number"]


class DealerInventoryFilter(filters.FilterSet):
    dealer = CharFilterInFilter(field_name="dealer__name", lookup_expr="in")
    model = CharFilterInFilter(field_name="model__name", lookup_expr="in")
    price = filters.NumberFilter(field_name="price")

    class Meta:
        model = DealerInventory
        fields = ["dealer", "model", "price"]


class BuyingHistoryDealerFilter(filters.FilterSet):
    dealership = CharFilterInFilter(
        field_name="dealership__name",
        lookup_expr="in")
    dealer = CharFilterInFilter(field_name="dealer__name", lookup_expr="in")
    car = CharFilterInFilter(field_name="car__name", lookup_expr="in")

    class Meta:
        model = BuyingHistoryDealer
        fields = ["dealership", "dealer", "car"]


class PromotionDealershipFilter(filters.FilterSet):
    name = CharFilterInFilter(field_name="name", lookup_expr="in")
    dealership = CharFilterInFilter(
        field_name="dealership__name",
        lookup_expr="in")
    model = CharFilterInFilter(field_name="model__name", lookup_expr="in")

    class Meta:
        model = PromotionDealership
        fields = ["name", "dealership", "model"]


class PromotionDealerFilter(filters.FilterSet):
    name = CharFilterInFilter(field_name="name", lookup_expr="in")
    dealer = CharFilterInFilter(field_name="dealer__name", lookup_expr="in")
    model = CharFilterInFilter(field_name="model__name", lookup_expr="in")

    class Meta:
        model = PromotionDealer
        fields = ["name", "dealer", "model"]
