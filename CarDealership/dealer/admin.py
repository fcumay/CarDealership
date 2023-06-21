from django.contrib import admin
from .models import *


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'amount_of_client', 'location', 'contact_number', 'is_active', 'created_at',
                    'updated_at']


#
@admin.register(DealerInventory)
class DealerInventoryAdmin(admin.ModelAdmin):
    list_display = ['dealer', 'car', 'price', 'is_active', 'created_at', 'updated_at', ]


@admin.register(PromotionDealer)
class PromotionDealerAdmin(admin.ModelAdmin):
    list_display = ['dealer', 'car', 'name', 'date_start', 'date_finish', 'description', 'percentage', 'is_active',
                    'created_at', 'updated_at']
