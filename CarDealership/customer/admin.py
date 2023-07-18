from django.contrib import admin
from .models import Customer, BuyingHistoryCustomer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "name",
        "role",
        "balance",
        "location",
        "contact_number",
        "dob",
    )

    def get_location_display(self, obj):
        return str(obj.location)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            password = form.cleaned_data.get("password")
            obj.set_password(password)
        obj.save()


@admin.register(BuyingHistoryCustomer)
class BuyingHistoryCustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "dealership", "car", "price", "created_at")
