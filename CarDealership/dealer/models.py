from core.models import *
from django_countries.fields import CountryField


class Dealer(BaseModel):
    id_dealer = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    amount_of_client = models.PositiveIntegerField(default=0)
    location = CountryField()
    contact_number = models.CharField(max_length=13)

    def __str__(self):
        return self.name


class DealerInventory(BaseModel):
    id_inv_dealer = models.AutoField(primary_key=True)
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.dealer.name} - {self.car.name}: ${self.price}"


class PromotionDealer(Promotion):
    id_promo_dealer = models.AutoField(primary_key=True)
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f"Promotion: {self.name} - Dealer: {self.dealer}"
