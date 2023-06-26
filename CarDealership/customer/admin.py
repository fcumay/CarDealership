from django.contrib import admin
from .models import Customer, BuyingHistoryCustomer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'name', 'balance', 'location', 'contact_number', 'age', 'is_active', 'created_at', 'updated_at')


@admin.register(BuyingHistoryCustomer)
class BuyingHistoryCustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'dealership', 'car', 'price', 'created_at')
