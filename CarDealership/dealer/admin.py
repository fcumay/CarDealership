from django.contrib import admin
from .models import Dealer, BuyingHistoryDealer, PromotionDealership, PromotionDealer


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'amount_of_client', 'location', 'contact_number', 'discount_program', 'is_active', 'created_at',
        'updated_at')


@admin.register(BuyingHistoryDealer)
class BuyingHistoryDealerAdmin(admin.ModelAdmin):
    list_display = ('id', 'dealership', 'dealer', 'car', 'price', 'created_at')


@admin.register(PromotionDealership)
class PromotionDealershipAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'dealership', 'model', 'date_start', 'date_finish', 'description', 'percentage', 'created_at')


@admin.register(PromotionDealer)
class PromotionDealerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'dealer', 'model', 'date_start', 'date_finish', 'description', 'percentage', 'created_at')
