from core.models import *
from dealership.models import Dealership
from django_countries.fields import CountryField


class Customer(BaseModel):
    id_customer = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    balance = models.PositiveIntegerField(default=0)  # positive
    location = CountryField()
    contact_number = models.CharField(max_length=13)
    age = models.IntegerField()

    def __str__(self):
        return self.name


class BuyingHistoryCustomer(BaseModel):
    id_history_customer = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.customer} bought {self.car} from {self.dealership}"
