from django.contrib import admin
from .models import Characteristic, Dealer, Customer, Automobile, Dealership, ListOfAutomobilesDealer, \
    ListOfAutomobilesDealership, BuyingHistoryDealer, BuyingHistoryCustomer, Cooperation, Promotion, \
    PromotionDealer, PromotionDealership, RegularVisitor

@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ['name','year','amount_of_client']


@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    list_display = ['characteristic']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'balance', 'location', 'contact_number', 'is_active', 'created_at', 'updated_at']


@admin.register(Automobile)
class AutomobileAdmin(admin.ModelAdmin):
    list_display = ['id', 'model', 'characteristics', 'is_active', 'created_at', 'updated_at']


@admin.register(Dealership)
class DealershipAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'balance', 'location', 'characteristics', 'is_active', 'created_at', 'updated_at']


@admin.register(ListOfAutomobilesDealer)
class ListOfAutomobilesDealerAdmin(admin.ModelAdmin):
    list_display = ['id', 'dealer', 'automobile', 'price', 'is_active', 'created_at', 'updated_at']


@admin.register(ListOfAutomobilesDealership)
class ListOfAutomobilesDealershipAdmin(admin.ModelAdmin):
    list_display = ['id', 'dealership', 'automobile', 'price', 'amount', 'is_active', 'created_at', 'updated_at']


@admin.register(BuyingHistoryDealer)
class BuyingHistoryDealerAdmin(admin.ModelAdmin):
    list_display = ['id', 'dealer', 'automobile', 'dealership', 'is_active', 'created_at', 'updated_at']


@admin.register(BuyingHistoryCustomer)
class BuyingHistoryCustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'dealership', 'automobile', 'is_active', 'created_at', 'updated_at']


@admin.register(Cooperation)
class CooperationAdmin(admin.ModelAdmin):
    list_display = ['id', 'dealership', 'dealer', 'automobile', 'is_active', 'created_at', 'updated_at']


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'date_start', 'date_finish', 'percentage', 'is_active', 'created_at', 'updated_at']


@admin.register(PromotionDealer)
class PromotionDealerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'date_start', 'date_finish', 'percentage', 'dealer', 'automobile', 'is_active', 'created_at', 'updated_at']


@admin.register(PromotionDealership)
class PromotionDealershipAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'date_start', 'date_finish', 'percentage', 'dealership', 'automobile', 'is_active', 'created_at', 'updated_at']


@admin.register(RegularVisitor)
class RegularVisitorAdmin(admin.ModelAdmin):
    list_display = ['id', 'dealership', 'customer', 'is_active', 'created_at', 'updated_at']
