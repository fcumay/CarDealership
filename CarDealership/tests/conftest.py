import pytest
from rest_framework.test import APIClient
from dealership import models as dealership
from customer import models as customer


@pytest.fixture
def user(client):
    register_payload = {
        "name": "user6",
        "email": "user6@gmail.com",
        "password": "12345678",
        "re_password": "12345678",
        "role": "customer"
    }
    response = client.post('/auth/user/', register_payload)
    id = response.json()["id"]
    user_payload = {
        "email": register_payload["email"],
        "password": register_payload["password"]
    }

    auth_response = client.post('/api/token/', user_payload)
    access_token = auth_response.json()["access"]
    user_payload["token"] = access_token
    user_payload["id"] = id
    return user_payload


@pytest.fixture
def user_admin(client):
    register_payload = {
        "name": "superadmin",
        "email": "superadmin7@example.com",
        "password": "12345678",
        "re_password": "12345678",
        "role": "superuser"
    }
    response = client.post('/auth/user/', register_payload)

    user_payload = {
        "email": register_payload["email"],
        "password": register_payload["password"]
    }

    auth_response = client.post('/api/token/', user_payload)
    access_token = auth_response.json()["access"]
    user_payload["token"] = access_token
    return user_payload


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user_client(user, client):
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {user["token"]}')
    return client


@pytest.fixture
def admin_client(user_admin, client):
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_admin["token"]}')
    return client


@pytest.fixture
def ford_brand():
    return dealership.Brand.objects.create(name="Ford")


@pytest.fixture
def mustang_model(ford_brand):
    return dealership.cker


@pytest.fixture
def new_dealership(ford_brand):
    dealership_admin = customer.Customer.objects.create_dealership_admin(email="da1@gmail.com", name="da1",
                                                                         password="12345678")
    return dealership.Dealership.objects.create(name="AutoHub", brand=ford_brand, balance=1000, location="BY",
                                                contact_number="+375445854055", discount_program=10,
                                                owner=dealership_admin)


@pytest.fixture
def new_car(mustang_model, new_dealership):
    customer1 = customer.Customer.objects.create_customer(email="user1@gmail.com", name="user1", location="BY",
                                                          contact_number="+375445854055", dob="2003-05-11",
                                                          password="12345678")
    return dealership.Car.objects.create(name="Ford Mustang", model=mustang_model, customer=customer1,
                                         dealership=new_dealership, price=10)
