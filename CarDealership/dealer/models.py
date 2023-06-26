from django.db import models

from django_countries.fields import CountryField


class Dealer(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    amount_of_client = models.PositiveIntegerField(default=0)
    location = CountryField()
    contact_number = models.CharField(max_length=13)
    discount_program = models.IntegerField()

    def __str__(self):
        return self.name


class BuyingHistoryDealer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.AutoField(primary_key=True)
    dealership = models.ForeignKey('dealership.Dealership', on_delete=models.CASCADE)
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    car = models.ForeignKey('dealership.Car', on_delete=models.CASCADE)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.dealership} bought {self.car} from {self.dealer}"


class Promotion(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    date_start = models.DateTimeField()
    date_finish = models.DateTimeField()
    description = models.CharField(max_length=500)
    percentage = models.IntegerField(default=0)

    class Meta:
        abstract = True


class PromotionDealership(Promotion):
    id = models.AutoField(primary_key=True)
    dealership = models.ForeignKey('dealership.Dealership', on_delete=models.CASCADE)
    car = models.ForeignKey('dealership.Car', on_delete=models.CASCADE)

    def __str__(self):
        return f"Promotion: {self.name} - Dealership: {self.dealership}"


class PromotionDealer(Promotion):
    id = models.AutoField(primary_key=True)
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    car = models.ForeignKey('dealership.Car', on_delete=models.CASCADE)

    def __str__(self):
        return f"Promotion: {self.name} - Dealership: {self.dealer}"
