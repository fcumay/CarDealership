from django_countries import countries
from django.contrib.auth import get_user_model
from django_countries.serializers import CountryFieldMixin
from customer.models import Customer, BuyingHistoryCustomer
from rest_framework import serializers
from dealership.models import Dealership

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
    location = serializers.CharField(source="get_location_display")

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

    def update(self, instance, validated_data):
        validated_data.pop('email', self.instance.email)
        return super().update(instance, validated_data)


class BuyingHistoryCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyingHistoryCustomer
        fields = ("id", "created_at", "customer", "dealership", "car", "price")

    def to_internal_value(self, data):
        modified_data = self.modify_data(data)
        return super().to_internal_value(modified_data)

    def modify_data(self, data):
        modified_data = data.copy()
        customer = modified_data.get("customer")
        dealership = modified_data.get("dealership")
        car = modified_data.get("car")
        try:
            if customer:
                customer = Customer.objects.get(name=customer)
                modified_data["customer"] = customer.id
            if dealership:
                dealership = Dealership.objects.get(name=dealership)
                modified_data["dealership"] = dealership.id
            if car:
                car = Dealership.objects.get(name=car)
                modified_data["car"] = car.id
        except BaseException:
            raise serializers.ValidationError("Input valid data")
        return modified_data
