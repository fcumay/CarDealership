from django.contrib.auth import get_user_model
from django_countries.serializers import CountryFieldMixin
from customer.models import Customer, BuyingHistoryCustomer
from rest_framework import serializers
from dealership.models import Dealership, Car

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = User
        fields = ("id", "name", "email", "password", "re_password", "role")
        extra_kwargs = {
            "password": {"write_only": True},
            "re_password": {"write_only": True},
        }

    def validate(self, data):
        password = data.get("password")
        re_password = data.get("re_password")
        if password and re_password and password != re_password:
            raise serializers.ValidationError("Password mismatch")
        if password and len(password) < 8:
            raise serializers.ValidationError(
                "The password must contain at least 8 characters"
            )
        return data

    def create(self, validated_data):
        if validated_data["role"] == "customer":
            return User.objects.create_customer(
                email=validated_data["email"].lower(),
                name=validated_data["name"],
                password=validated_data["password"],
            )
        elif validated_data["role"] == "dealership_admin":
            return User.objects.create_dealership_admin(
                email=validated_data["email"].lower(),
                name=validated_data["name"],
                password=validated_data["password"],
            )


class InformationSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            "id",
            "name",
            "email",
            "balance",
            "location",
            "contact_number",
            "dob")

    def update(self, instance, validated_data):
        validated_data.pop('email', self.instance.email)
        return super().update(instance, validated_data)


class BuyingHistoryCustomerSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all())
    dealership = serializers.PrimaryKeyRelatedField(
        queryset=Dealership.objects.all())
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())

    class Meta:
        model = BuyingHistoryCustomer
        fields = ("id", "created_at", "customer", "dealership", "car", "price")
