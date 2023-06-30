from django.contrib import admin
from .models import Customer, BuyingHistoryCustomer, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "name")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "balance", "location", "contact_number", "age")


@admin.register(BuyingHistoryCustomer)
class BuyingHistoryCustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "dealership", "car", "price", "created_at")
