from rest_framework import serializers
from django.contrib.auth import get_user_model
from django_countries.serializers import CountryFieldMixin
from customer.models import Customer, BuyingHistoryCustomer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "email",
            "role",
        )


class CustomerSerializer(CountryFieldMixin, serializers.ModelSerializer):
    location = serializers.CharField(source="get_location_display")

    class Meta:
        model = Customer
        fields = ("name", "email", "balance", "location", "contact_number", "dob")


class BuyingHistoryCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyingHistoryCustomer
        fields = "__all__"
