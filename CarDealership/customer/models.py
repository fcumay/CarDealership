from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django_countries.fields import CountryField


class UserAccountManager(BaseUserManager):
    def create_customer(
        self, email, name, balance, location, contact_number, age, password=None
    ):
        user = self.model(
            email=email, name=name, is_active=True, is_staff=False, is_superuser=False
        )
        user.set_password(password)
        user.save()

        customer = Customer.objects.create(
            user=user,
            balance=balance,
            location=location,
            contact_number=contact_number,
            age=age,
        )
        return user

    def create_dealership_admin(self, email, name, password=None):
        user = self.model(email=email, name=name, is_dealership_admin=True)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, password=None):
        user = self.model(email=email, name=name, is_superuser=True, is_staff=True)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UserAccountManager()


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer")
    balance = models.PositiveIntegerField(default=0)
    location = CountryField()
    contact_number = models.CharField(max_length=20)
    age = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.name


class BuyingHistoryCustomer(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    dealership = models.ForeignKey("dealership.Dealership", on_delete=models.CASCADE)
    car = models.ForeignKey("dealership.Car", on_delete=models.CASCADE)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.customer} bought {self.car} from {self.dealership}"
