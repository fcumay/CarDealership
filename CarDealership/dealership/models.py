from core.models import *
from dealer.models import Dealer
from django_countries.fields import CountryField


class Dealership(BaseModel, BaseCharacteristic):
    id_dealership = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    balance = models.IntegerField(default=0)
    location = CountryField(max_length=15)
    contact_number = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class DealershipInventory(BaseModel):
    id_inv_dealership = models.AutoField(primary_key=True)
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.dealership.name} - {self.car.name}: {self.quantity}"


class BuyingHistoryDealership(BaseModel):
    id_history_dealership = models.AutoField(primary_key=True)
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.dealership} bought {self.car} from {self.dealer}"


class PromotionDealership(Promotion):
    id_promo_dealership = models.AutoField(primary_key=True)
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f"Promotion: {self.name} - Dealership: {self.dealership}"
