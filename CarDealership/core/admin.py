from django.contrib import admin
from .models import Car

@admin.register(Car)
class AutomobileAdmin(admin.ModelAdmin):
    list_display = ['model', 'is_active','created_at','updated_at', 'drivetrain','engine', 'bodytype', 'transmission']

# Register your models here.
