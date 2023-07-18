from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin
from .models import Dealer, DealerInventory, PromotionDealership, PromotionDealer


class DealerSerializer(CountryFieldMixin, serializers.ModelSerializer):
    location = serializers.CharField(source="get_location_display")

    class Meta:
        model = Dealer
        fields = (
            "name",
            "amount_of_client",
            "location",
            "contact_number",
            "discount_program",
        )


class DealerInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DealerInventory
        fields = "__all__"


class PromotionDealershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionDealership
        fields = "__all__"


class PromotionDealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionDealer
        fields = "__all__"
