from django_countries import countries
from customer.models import Customer
from .models import Brand, Model, Car
from rest_framework import serializers
from .models import Dealership
from django.shortcuts import get_object_or_404


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
        if brand:
            brand = get_object_or_404(Brand, name=brand)
            modified_data["brand"] = brand.id
        if owner:
            owner = get_object_or_404(Customer, email=owner)
            modified_data["owner"] = owner.id
        if location:
            for code, name in countries:
                if name == location:
                    location = code
            modified_data["location"] = location
        return modified_data


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            "id",
            "name",
        )


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

    def to_internal_value(self, data):
        modified_data = self.modify_data(data)
        return super().to_internal_value(modified_data)

    def modify_data(self, data):
        modified_data = data.copy()
        brand = modified_data.get("brand")
        if brand:
            brand = get_object_or_404(Brand, name=brand)
            modified_data["brand"] = brand.id
        return modified_data


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ("id", "name", "model", "customer", "dealership", "price")

    def to_internal_value(self, data):
        modified_data = self.modify_data(data)
        return super().to_internal_value(modified_data)

    def modify_data(self, data):
        modified_data = data.copy()
        model = modified_data.get("model")
        customer = modified_data.get("customer")
        dealership = modified_data.get("dealership")
        if model:
            model = get_object_or_404(Model, name=model)
            modified_data["model"] = model.id
        if customer:
            customer = get_object_or_404(Customer, email=customer)
            modified_data["customer"] = customer.id
        if dealership:
            dealership = get_object_or_404(Dealership, name=dealership)
            modified_data["dealership"] = dealership.id
        return modified_data

    def create(self, validated_data):
        name = validated_data.get('name')
        model = validated_data.get('model')
        dealership = validated_data.get('dealership')
        price = validated_data.get('price')
        car = Car(name=name, model=model, dealership=dealership, price=price)
        car.save()
        return car

    def update(self, instance, validated_data):
        customer = validated_data.get('customer')
        instance.customer = customer
        instance.dealership = None
        instance.save()
        return instance
