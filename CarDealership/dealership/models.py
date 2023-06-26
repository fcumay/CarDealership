from django.db import models

from customer.models import Customer
from django_countries.fields import CountryField

from dealer.models import Dealer


class DrivetrainChoices(models.TextChoices):
    FWD = 'FWD', 'FWD'
    AWD = 'AWD', 'AWD'
    RWD = 'RWD', 'RWD'
    WD4 = '4WD', '4WD'


class FuelTypeChoices(models.TextChoices):
    DIESEL = 'Diesel', 'Diesel'
    PETROL = 'Petrol', 'Petrol'
    ELECTRIC = 'Electric', 'Electric'
    NATURAL = 'Natural', 'Natural'
    GAS = 'Gas', 'Gas'
    HYDROGEN = 'Hydrogen', 'Hydrogen'
    LPG = 'LPG', 'LPG'
    FLEX_FUEL = 'Flex-fuel', 'Flex-fuel'


class BodyTypeChoices(models.TextChoices):
    HATCHBACK = 'Hatchback', 'Hatchback'
    SEDAN = 'Sedan', 'Sedan'
    SUV = 'SUV', 'SUV'
    MUV = 'MUV', 'MUV'
    COUPE = 'Coupe', 'Coupe'
    CONVERTIBLE = 'Convertible', 'Convertible'
    PICKUP = 'Pickup', 'Pickup'
    TRUCK = 'Truck', 'Truck'


class TransmissionChoices(models.TextChoices):
    AUTOMATIC = 'automatic', 'Automatic'
    MANUAL = 'manual', 'Manual'
    CVT = 'CVT', 'CVT'


class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Dealership(models.Model):
    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    balance = models.PositiveIntegerField(default=0)
    location = CountryField(max_length=15)
    contact_number = models.CharField(max_length=200)
    discount_program = models.IntegerField()

    def __str__(self):
        return self.name


class Car(models.Model):
    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.CharField(max_length=100)
    drivetrain = models.CharField(max_length=20, choices=DrivetrainChoices.choices, default=DrivetrainChoices.FWD)
    engine = models.CharField(max_length=20, choices=FuelTypeChoices.choices, default=FuelTypeChoices.PETROL)
    bodytype = models.CharField(max_length=20, choices=BodyTypeChoices.choices, default=BodyTypeChoices.SEDAN)
    transmission = models.CharField(max_length=20, choices=TransmissionChoices.choices,
                                    default=TransmissionChoices.AUTOMATIC)

    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, default=None, blank=True)
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE, null=True, blank=True)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.model
