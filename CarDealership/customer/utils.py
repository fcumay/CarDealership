import random
import string
from django.db.models import Sum
from .models import Customer, BuyingHistoryCustomer
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import send_mail
from django.db.models import Prefetch


def generate_verification_token():
    characters = string.ascii_letters + string.digits
    token = ''.join(random.choice(characters) for _ in range(6))
    return token


def send_email_link(token, user):
    verification_link = f"http://localhost:8001/auth/user/verify_email/?token={token}"
    send_mail(
        "Email Verification",
        f"Please verify your email by clicking this link: {verification_link}",
        "voyshnismaya@gmail.com",
        [user.email],
        fail_silently=False,
    )
    return True


def send_password_reset_link(user, email):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    reset_url = reverse(
        "password_reset_confirm",
        kwargs={
            "uidb64": uid,
            "token": token})

    send_mail(
        "Password Reset",
        f"Use the following link to reset your password: http://localhost:8001/{reset_url}",
        "voyshnismaya@gmail.com",
        [email],
        fail_silently=False,
    )


def get_customer(id):
    return Customer.objects.get(id=id)


def get_statistic(customer):
    buying_history_prefetch = Prefetch('buyinghistorycustomer_set',
                                       queryset=BuyingHistoryCustomer.objects.select_related('car'))
    customer_with_history = Customer.objects.prefetch_related(
        buying_history_prefetch).get(email=customer.email)

    total_spent = customer_with_history.buyinghistorycustomer_set.aggregate(total_spent=Sum('price'))[
        'total_spent']

    cars = [
        entry.car.name for entry in customer_with_history.buyinghistorycustomer_set.all()]

    return {'cars': cars, 'totally_spend': total_spent}
