import pytest
from dealership import models


@pytest.mark.django_db
def test_create_dealership(admin_client, new_dealership):
    payload = {
        "name": "McQueen",
        "brand": new_dealership.brand.id,
        "balance": 2147483647,
        "location": "AF",
        "contact_number": "+375445854055",
        "discount_program": 10,
        "owner": new_dealership.owner.id
    }

    response = admin_client.post("/api/dealership/", payload)
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_dealership_403(user_client, new_dealership):
    payload = {
        "name": "McQueen",
        "brand": new_dealership.brand.id,
        "balance": 2147483647,
        "location": "AF",
        "contact_number": "+375445854055",
        "discount_program": 10,
        "owner": new_dealership.owner.id
    }

    response = user_client.post("/api/dealership/", payload)
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_dealerships_admin(admin_client, new_dealership):
    response = admin_client.get(f"/api/dealership/")
    assert response.status_code == 200
    data = response.data
    assert data[0]["balance"] == new_dealership.balance


@pytest.mark.django_db
def test_get_dealerships_dadmin(admin_client, new_dealership):
    response = admin_client.post('/auth/user/', {"name": "da2", "email": "da2@gmail.com", "password": "12345678",
                                                 "re_password": "12345678", "role": "dealership_admin"})

    auth_response = admin_client.post(
        '/api/token/', {"email": "da2@gmail.com", "password": "12345678"})
    access_token = auth_response.json()["access"]
    admin_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    dealership1 = models.Dealership.objects.create(name="McQueen", brand=new_dealership.brand, balance=1000,
                                                   location="BY", contact_number="+375445854055", discount_program=10,
                                                   owner=models.Customer.objects.get(email="da2@gmail.com"))

    response = admin_client.get(f"/api/dealership/{dealership1.id}/")
    data = response.data
    assert "balance" in data

    response = admin_client.get(f"/api/dealership/{new_dealership.id}/")
    data = response.data
    assert "balance" not in data and "owner" not in data


@pytest.mark.django_db
def test_update_dealership_admin(admin_client, new_dealership):
    payload = {
        "balance": 111,
    }

    response = admin_client.patch(
        f"/api/dealership/{new_dealership.id}/", payload)

    assert response.status_code == 200

    new_dealership.refresh_from_db()

    assert new_dealership.balance == 111


@pytest.mark.django_db
def test_update_dealership_dadmin(admin_client, new_dealership):
    response = admin_client.post('/auth/user/', {"name": "da2", "email": "da2@gmail.com", "password": "12345678",
                                                 "re_password": "12345678", "role": "dealership_admin"})

    auth_response = admin_client.post(
        '/api/token/', {"email": "da2@gmail.com", "password": "12345678"})
    access_token = auth_response.json()["access"]
    admin_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    dealership = models.Dealership.objects.create(name="McQueen", brand=new_dealership.brand, balance=1000,
                                                  location="BY", contact_number="+375445854055", discount_program=10,
                                                  owner=models.Customer.objects.get(email="da2@gmail.com"))

    payload = {
        "name": "NewName",
        "balance": 111,
    }

    response = admin_client.patch(f"/api/dealership/{dealership.id}/", payload)
    assert response.status_code == 200

    dealership.refresh_from_db()

    assert dealership.balance == 1000
    assert dealership.name == "NewName"


@pytest.mark.django_db
def test_delete_dealership(admin_client, new_dealership):
    response = admin_client.delete(f"/api/dealership/{new_dealership.id}/")
    assert response.status_code == 204
    new_dealership.refresh_from_db()
    assert new_dealership.is_active == False


@pytest.mark.django_db
def test_delete_dealership_403(user_client, new_dealership):
    response = user_client.delete(f"/api/dealership/{new_dealership.id}/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_statistic(user_client, new_dealership):
    response = user_client.get(
        f"/api/dealership/statistic/{new_dealership.id}")
    assert response.status_code == 200
    data = response.data
    assert len(data) == 3
