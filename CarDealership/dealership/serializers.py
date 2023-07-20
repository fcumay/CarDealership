from customer.models import Customer
from .models import  Brand
from django_countries import countries
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
            "owner"
        )
    # def to_internal_value(self, data):
    #     modified_data = self.modify_data(data)
    #     return super().to_internal_value(modified_data)
    #
    # def modify_data(self,data):
    #     modified_data = data.copy()
    #     brand = modified_data.get("brand")
    #     owner = modified_data.get("owner")
    #     location = modified_data.get("location")
    #     if brand:
    #         brand = Brand.objects.get(name=brand)
    #         modified_data["brand"] = brand.id
    #     if owner:
    #         owner = Customer.objects.get(email=owner)
    #         modified_data["owner"] = owner.id
    #     if location:
    #         for code, name in countries:
    #             if name == location:
    #                 location=code
    #         modified_data["location"]=location
    #
    #     return modified_data




