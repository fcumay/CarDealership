from customer.models import Customer
from .models import Brand, Model, Car
from rest_framework import serializers
from .models import Dealership


class DealershipSerializer(serializers.ModelSerializer):
    brand = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.filter(is_active=True))
    owner = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.filter(is_active=True))

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

    def update(self, instance, validated_data):
        request = self.context.get("request", None)
        if not request.user.is_superuser:
            if "owner" in validated_data:
                validated_data.pop("owner")
            if "balance" in validated_data:
                validated_data.pop("balance")
        return super().update(instance, validated_data)

    def partial_update(self, instance, validated_data):
        request = self.context.get("request", None)
        if not request.user.is_superuser:
            if "owner" in validated_data:
                validated_data.pop("owner")
            if "balance" in validated_data:
                validated_data.pop("balance")
        return super().partial_update(instance, validated_data)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            "id",
            "name",
        )


class ModelSerializer(serializers.ModelSerializer):
    brand = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.filter(is_active=True))

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


class CarSerializer(serializers.ModelSerializer):
    model = serializers.PrimaryKeyRelatedField(
        queryset=Model.objects.filter(is_active=True))
    dealership = serializers.PrimaryKeyRelatedField(
        queryset=Dealership.objects.filter(is_active=True))

    class Meta:
        model = Car
        fields = ("id", "name", "model", "dealership", "price")

    def update(self, instance, validated_data):
        request = self.context.get("request", None)
        if not request.user.is_superuser:
            if "name" in validated_data:
                validated_data.pop("name")
            if "model" in validated_data:
                validated_data.pop("model")
            if "customer" in validated_data:
                validated_data.pop("customer")
            if "dealership" in validated_data:
                validated_data.pop("dealership")
        return super().update(instance, validated_data)


class OfferSerializer(serializers.Serializer):
    model = serializers.CharField()
    price = serializers.IntegerField()
