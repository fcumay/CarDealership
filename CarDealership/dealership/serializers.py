from django_countries import countries

from customer.models import Customer, RoleChoices
from .models import Brand, Model, Car
from rest_framework import serializers
from .models import Dealership


class DealershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealership
        fields = (
            "id",
            "name",
            "brand",
            "balance",
            "location",
            "contact_number",
            "discount_program",
            "owner",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request", None)
        if request and not (
            request.user.is_superuser or request.user.email == instance.owner.email
        ):
            data.pop("id", None)
            data.pop("balance", None)
            data.pop("owner", None)
        return data

    def to_internal_value(self, data):
        modified_data = self.modify_data(data)
        return super().to_internal_value(modified_data)

    def modify_data(self, data):
        modified_data = data.copy()
        brand = modified_data.get("brand")
        owner = modified_data.get("owner")
        location = modified_data.get("location")
        try:
            if brand:
                brand = Brand.objects.get(name=brand)
                modified_data["brand"] = brand.id
            if owner:
                owner = Customer.objects.get(email=owner)
                modified_data["owner"] = owner.id
            if location:
                for code, name in countries:
                    if name == location:
                        location = code
                modified_data["location"] = location
        except BaseException:
            raise serializers.ValidationError("Input valid data")
        return modified_data


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            "id",
            "name",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request", None)
        if request and not request.user.is_superuser:
            data.pop("id", None)
        return data


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = (
            "id",
            "name",
            "brand",
            "drivetrain",
            "engine",
            "bodytype",
            "transmission",
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
        brand = modified_data.get("brand")
        try:
            if brand:
                brand = Brand.objects.get(name=brand)
                modified_data["brand"] = brand.id
        except BaseException:
            raise serializers.ValidationError("Input valid data")
        return modified_data


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ("id", "name", "model", "customer", "dealership", "price")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request", None)
        if request and not request.user.is_superuser:
            data.pop("id", None)
            data.pop("customer", None)
        return data

    def to_internal_value(self, data):
        modified_data = self.modify_data(data)
        return super().to_internal_value(modified_data)

    def modify_data(self, data):
        modified_data = data.copy()
        model = modified_data.get("model")
        customer = modified_data.get("customer")
        dealership = modified_data.get("dealership")
        try:
            if model:
                model = Model.objects.get(name=model)
                modified_data["model"] = model.id
            if customer:
                customer = Customer.objects.get(email=customer)
                modified_data["customer"] = customer.id
            if dealership:
                dealership = Dealership.objects.get(name=dealership)
                modified_data["dealership"] = dealership.id
        except BaseException:
            raise serializers.ValidationError("Input valid data")
        return modified_data
