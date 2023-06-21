from django.contrib import admin
from .models import *


@admin.register(Dealership)
class DealerAdmin(admin.ModelAdmin):
    list_display = ['name', 'balance', 'location', 'contact_number', 'is_active', 'created_at', 'updated_at',
                    'drivetrain', 'engine', 'bodytype', 'transmission']


#
@admin.register(DealershipInventory)
class DealerInventoryAdmin(admin.ModelAdmin):
    list_display = ['dealership', 'car', 'quantity', 'price', 'is_active', 'created_at', 'updated_at']


@admin.register(BuyingHistoryDealership)
class BuyingHistoryDealershipAdmin(admin.ModelAdmin):
    list_display = ['dealership', 'car', 'dealer', 'price', 'is_active', 'created_at', 'updated_at']


@admin.register(PromotionDealership)
class PromotionDealerAdmin(admin.ModelAdmin):
    list_display = ['dealership', 'car', 'name', 'date_start', 'date_finish', 'description', 'percentage', 'is_active',
                    'created_at', 'updated_at', ]
