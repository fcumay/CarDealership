from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class RoleChoices(models.TextChoices):
    is_customer = "customer", "customer"
    is_dealership_admin = "dealership_admin", "dealership_admin"
    is_superuser = "superuser", "superuser"


class UserAccountManager(BaseUserManager):
    def create_customer(
            self,
            email,
            name,
            location=None,
            contact_number=None,
            dob=None,
            password=None,
    ):
        user = self.model(
            email=email,
            name=name,
            is_active=True,
            balance=15,
            location=location,
            contact_number=contact_number,
            dob=dob,
        )
        user.set_password(password)
        user.save()
        return user

    def create_dealership_admin(self, email, name, password=None):
        user = self.model(
            email=email,
            name=name,
            role=RoleChoices.is_dealership_admin)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, password=None):
        user = self.model(
            email=email,
            name=name,
            role=RoleChoices.is_superuser)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class Customer(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    role = models.CharField(
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.is_customer,
    )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    balance = models.PositiveIntegerField(default=0, null=True, blank=True)
    location = CountryField(max_length=15, null=True, blank=True)
    contact_number = PhoneNumberField(null=True, blank=True)
    dob = models.DateField(max_length=8, null=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UserAccountManager()

    def __str__(self):
        return self.name


class BuyingHistoryCustomer(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT)
    dealership = models.ForeignKey(
        "dealership.Dealership",
        on_delete=models.CASCADE)
    car = models.ForeignKey("dealership.Car", on_delete=models.RESTRICT)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.customer} bought {self.car} from {self.dealership}"
