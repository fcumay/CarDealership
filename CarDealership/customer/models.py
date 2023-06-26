from django.db import models
from django_countries.fields import CountryField


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    balance = models.PositiveIntegerField(default=0)  # positive
    location = CountryField()
    contact_number = models.CharField(max_length=13)
    age = models.IntegerField()

    def __str__(self):
        return self.name


class BuyingHistoryCustomer(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    dealership = models.ForeignKey('dealership.Dealership', on_delete=models.CASCADE)
    car = models.ForeignKey('dealership.Car', on_delete=models.CASCADE)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.customer} bought {self.car} from {self.dealership}"
