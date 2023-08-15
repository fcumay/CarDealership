from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin

from dealership.models import Model, Dealership, Car
from .models import (
    Dealer,
    DealerInventory,
    PromotionDealership,
    PromotionDealer,
    BuyingHistoryDealer,
)


class DealerSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Dealer
        fields = (
            "id",
            "name",
            "amount_of_client",
            "location",
            "contact_number",
            "discount_program",
        )


class DealerInventorySerializer(serializers.ModelSerializer):
    dealer = serializers.PrimaryKeyRelatedField(queryset=Dealer.objects.all())
    model = serializers.PrimaryKeyRelatedField(queryset=Model.objects.all())

    class Meta:
        model = DealerInventory
        fields = (
            "id",
            "dealer",
            "model",
            "price",
        )


class BuyingHistoryDealerSerializer(serializers.ModelSerializer):
    dealership = serializers.PrimaryKeyRelatedField(
        queryset=Dealership.objects.all())
    dealer = serializers.PrimaryKeyRelatedField(queryset=Dealer.objects.all())
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())

    class Meta:
        model = BuyingHistoryDealer
        fields = (
            "id",
            "dealership",
            "dealer",
            "car",
            "price",
        )


class PromotionDealershipSerializer(serializers.ModelSerializer):
    dealership = serializers.PrimaryKeyRelatedField(
        queryset=Dealership.objects.all())
    model = serializers.PrimaryKeyRelatedField(queryset=Model.objects.all())

    class Meta:
        model = PromotionDealership
        fields = (
            "id",
            "name",
            "date_start",
            "date_finish",
            "description",
            "percentage",
            "dealership",
            "model",
        )


class PromotionDealerSerializer(serializers.ModelSerializer):
    dealer = serializers.PrimaryKeyRelatedField(queryset=Dealer.objects.all())
    model = serializers.PrimaryKeyRelatedField(queryset=Model.objects.all())

    class Meta:
        model = PromotionDealer
        fields = (
            "id",
            "name",
            "date_start",
            "date_finish",
            "description",
            "percentage",
            "dealer",
            "model",
        )
