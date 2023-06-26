from django.contrib import admin
from .models import Brand, Dealership, Car

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','is_active','created_at','updated_at')

@admin.register(Dealership)
class DealershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'brand', 'balance', 'location', 'contact_number', 'discount_program','is_active','created_at','updated_at')

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'model', 'drivetrain', 'engine', 'bodytype', 'transmission', 'dealer', 'customer', 'dealership', 'price','is_active','created_at','updated_at')


