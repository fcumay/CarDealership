from django.db import models


class BaseModel(models.Model):
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseCharacteristic(models.Model):
    DRIVETRAIN_CHOICES = ['FWD', 'AWD', 'RWD', '4WD']
    ENGINE_CHOICES = ['Diesel', 'Petrol', 'Electric', 'Natural', 'Gas', 'Hydrogen', 'LPG', 'Flex-fuel']
    BODYTYPE_CHOICES = ['Hatchback', 'Sedan', 'SUV', 'MUV', 'Coupe', 'Convertible', 'Pickup', 'Truck']
    TRANSMISSION_CHOICES = ['automatic', 'manual', 'CVT']

    drivetrain = models.CharField(max_length=10, choices=zip(DRIVETRAIN_CHOICES, DRIVETRAIN_CHOICES))
    engine = models.CharField(max_length=10, choices=zip(ENGINE_CHOICES, ENGINE_CHOICES))
    bodytype = models.CharField(max_length=20, choices=zip(BODYTYPE_CHOICES, BODYTYPE_CHOICES))
    transmission = models.CharField(max_length=10, choices=zip(TRANSMISSION_CHOICES, TRANSMISSION_CHOICES))

    class Meta:
        abstract = True


class Car(BaseModel, BaseCharacteristic):
    id_car = models.AutoField(primary_key=True)
    model = models.CharField(max_length=200)

    def __str__(self):
        return self.model


class Promotion(BaseModel):
    name = models.CharField(max_length=200)
    date_start = models.DateTimeField()
    date_finish = models.DateTimeField()
    description = models.CharField(max_length=500)
    percentage = models.IntegerField(default=0)

    def __str__(self):
        return self.name
