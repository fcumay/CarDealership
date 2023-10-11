import pytest


@pytest.mark.django_db
def test_register_customer(client):
    payload = {
        "name": "user9",
        "email": "user9@gmail.com",
        "password": "12345678",
        "re_password": "12345678",
        "role": "customer"
    }
    response = client.post('/auth/user/', payload)
    assert response.status_code == 201


@pytest.mark.django_db
def test_register_dealership_admin(admin_client):
    payload = {
        "name": "admin20",
        "email": "admin20@gmail.com",
        "password": "12345678",
        "re_password": "12345678",
        "role": "dealership_admin"
    }

    response = admin_client.post('/auth/user/', payload)
    assert response.status_code == 201


@pytest.mark.django_db
def test_register_dealership_admin_403(user_client):
    payload = {
        "name": "admin201",
        "email": "admin201@gmail.com",
        "password": "12345678",
        "re_password": "12345678",
        "role": "dealership_admin"
    }

    response = user_client.post('/auth/user/', payload)
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_me(user, client):
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {user["token"]}')
    response = client.get(f"/auth/info/{user['id']}/")
    assert response.status_code == 200
