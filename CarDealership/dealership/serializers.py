from customer.models import Customer
from .models import Brand, Model, Car
from rest_framework import serializers
from .models import Dealership


class DealershipSerializer(serializers.ModelSerializer):
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())
    owner = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

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


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            "id",
            "name",
        )


class ModelSerializer(serializers.ModelSerializer):
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())

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
    model = serializers.PrimaryKeyRelatedField(queryset=Model.objects.all())
    customer = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), allow_null=True)
    dealership = serializers.PrimaryKeyRelatedField(
        queryset=Dealership.objects.all())

    class Meta:
        model = Car
        fields = ("id", "name", "model", "customer", "dealership", "price")

    def create(self, validated_data):
        name = validated_data.get('name')
        model = validated_data.get('model')
        dealership = validated_data.get('dealership')
        price = validated_data.get('price')
        car = Car(
            name=name,
            model=model,
            dealership=dealership,
            price=price,
            customer=None)
        car.save()
        return car

    def update(self, instance, validated_data):
        customer = validated_data.get('customer')
        instance.customer = customer
        instance.dealership = None
        instance.save()
        return instance


class OfferSerializer(serializers.Serializer):
    model = serializers.CharField()
    price = serializers.IntegerField()