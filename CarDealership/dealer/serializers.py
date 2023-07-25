from django_countries import countries
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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request", None)
        if request and not request.user.is_superuser:
            data.pop("id", None)
        return data

    def to_internal_value(self, data):
        modified_data = self.modify_data(data)
        return super().to_internal_value(modified_data)

    def modify_data(self, data):
        modified_data = data.copy()
        location = modified_data.get("location")
        if location:
            for code, name in countries:
                if name == location:
                    location = code
            modified_data["location"] = location

        return modified_data


class DealerInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DealerInventory
        fields = (
            "id",
            "dealer",
            "model",
            "price",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request", None)
        if request and not request.user.is_superuser:
            data.pop("id", None)
        return data

    def to_internal_value(self, data):
        modified_data = self.modify_data(data)
        return super().to_internal_value(modified_data)

    def modify_data(self, data):
        modified_data = data.copy()
        dealer = modified_data.get("dealer")
        model = modified_data.get("model")
        if dealer:
            dealer = Dealer.objects.get(name=dealer)
            modified_data["dealer"] = dealer.id
        if model:
            model = Model.objects.get(name=model)
            modified_data["model"] = model.id

        return modified_data


class BuyingHistoryDealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyingHistoryDealer
        fields = (
            "id",
            "dealership",
            "dealer",
            "car",
            "price",
        )

    def to_internal_value(self, data):
        modified_data = self.modify_data(data)
        return super().to_internal_value(modified_data)

    def modify_data(self, data):
        modified_data = data.copy()
        dealership = modified_data.get("dealer")
        dealer = modified_data.get("dealer")
        car = modified_data.get("car")
        if dealership:
            dealership = Dealership.objects.get(name=dealership)
            modified_data["dealership"] = dealership.id
        if dealer:
            dealer = Dealer.objects.get(name=dealer)
            modified_data["dealer"] = dealer.id
        if car:
            car = Car.objects.get(name=car)
            modified_data["car"] = car.id
        return modified_data


class PromotionDealershipSerializer(serializers.ModelSerializer):
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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request", None)
        if request and not request.user.is_superuser:
            data.pop("id", None)
        return data

    def to_internal_value(self, data):
        modified_data = self.modify_data(data)
        return super().to_internal_value(modified_data)

    def modify_data(self, data):
        modified_data = data.copy()
        dealership = modified_data.get("dealership")
        model = modified_data.get("model")
        if dealership:
            dealership = Dealership.objects.get(name=dealership)
            modified_data["dealership"] = dealership.id
        if model:
            model = Model.objects.get(name=model)
            modified_data["model"] = model.id

        return modified_data


class PromotionDealerSerializer(serializers.ModelSerializer):
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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request", None)
        if request and not request.user.is_superuser:
            data.pop("id", None)
        return data

    def to_internal_value(self, data):
        modified_data = self.modify_data(data)
        return super().to_internal_value(modified_data)

    def modify_data(self, data):
        modified_data = data.copy()
        dealer = modified_data.get("dealer")
        model = modified_data.get("model")
        if dealer:
            dealer = Dealer.objects.get(name=dealer)
            modified_data["dealer"] = dealer.id
        if model:
            model = Model.objects.get(name=model)
            modified_data["model"] = model.id

        return modified_data
