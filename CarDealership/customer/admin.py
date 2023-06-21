from django.contrib import admin
from .models import *


@admin.register(Customer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ['name', 'balance', 'location', 'contact_number', 'age', 'is_active', 'created_at',
                    'updated_at']


@admin.register(BuyingHistoryCustomer)
class BuyingHistoryCustomerAdmin(admin.ModelAdmin):
    list_display = ['customer', 'car', 'dealership', 'price', 'is_active', 'created_at', 'updated_at']
