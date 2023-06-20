from django.db import models
from django_countries.fields import CountryField


class BaseModel(models.Model):
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Dealer(BaseModel):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    amount_of_client = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Characteristic(models.Model):
    characteristic = models.CharField(max_length=300)

    def __str__(self):
        return self.characteristic


class Customer(BaseModel):
    name = models.CharField(max_length=200)
    balance = models.IntegerField(default=0)
    location = CountryField()
    contact_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Automobile(BaseModel):
    model = models.CharField(max_length=200)
    characteristics = models.ForeignKey(Characteristic, on_delete=models.PROTECT)

    def __str__(self):
        return self.model


class Dealership(BaseModel):
    name = models.CharField(max_length=200)
    balance = models.IntegerField(default=0)
    location = CountryField()
    characteristics = models.ForeignKey(Characteristic, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class ListOfAutomobilesDealer(BaseModel):
    dealer = models.ForeignKey(Dealer, on_delete=models.PROTECT)
    automobile = models.ForeignKey(Automobile, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.dealer} - {self.automobile}"


class ListOfAutomobilesDealership(BaseModel):
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    automobile = models.ForeignKey(Automobile, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.dealership} - {self.automobile}"


class BuyingHistoryDealer(BaseModel):
    dealer = models.ForeignKey(Dealer, on_delete=models.PROTECT)
    automobile = models.ForeignKey(Automobile, on_delete=models.CASCADE)
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.dealer} bought {self.automobile} from {self.dealership}"


class BuyingHistoryCustomer(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    automobile = models.ForeignKey(Automobile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer} bought {self.automobile} from {self.dealership}"


class Cooperation(BaseModel):
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    automobile = models.ForeignKey(Automobile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cooperation: {self.dealership} - {self.dealer} - {self.automobile}"


class Promotion(BaseModel):
    name = models.CharField(max_length=200)
    date_start = models.DateTimeField()
    date_finish = models.DateTimeField()
    percentage = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class PromotionDealer(Promotion):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    automobile = models.ForeignKey(Automobile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Promotion: {self.name} - Dealer: {self.dealer}"


class PromotionDealership(Promotion):
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    automobile = models.ForeignKey(Automobile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Promotion: {self.name} - Dealership: {self.dealership}"


class RegularVisitor(BaseModel):
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer} - {self.dealership}"
