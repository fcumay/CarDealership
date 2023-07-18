from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin
from .models import Dealership, Brand, Model, Car


class DealershipSerializer(CountryFieldMixin, serializers.ModelSerializer):
    location = serializers.CharField(source="get_location_display")

    class Meta:
        model = Dealership
        fields = (
            "name",
            "brand",
            "balance",
            "location",
            "contact_number",
            "owner")


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ("name",)


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = (
            "name",
            "brand",
            "drivetrain",
            "engine",
            "bodytype",
            "transmission")


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = (
            "name",
            "model",
            "price",
        )
