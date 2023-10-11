import pytest

from dealership import models


@pytest.mark.django_db
def test_create_car(admin_client, new_car):
    payload = {"name": "Ford Focus",
               "model": new_car.model.id,
               "dealership": new_car.dealership.id,
               "price": 12}
    response = admin_client.post("/api/car/", payload)
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_car_403(user_client, new_car):
    payload = {"name": "Ford Focus",
               "model": new_car.model.id,
               "dealership": new_car.dealership.id,
               "price": 12}
    response = user_client.post("/api/car/", payload)
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_cars(admin_client, new_car):
    response = admin_client.get(f"/api/car/")
    assert response.status_code == 200
    data = response.data
    assert data[0]["name"] == new_car.name


@pytest.mark.django_db
def test_update_car_admin(admin_client, new_car):
    payload = {
        "name": "505",
        "price": 111,
    }

    response = admin_client.patch(f"/api/car/{new_car.id}/", payload)

    assert response.status_code == 200

    new_car.refresh_from_db()
    assert new_car.name == payload["name"]
    assert new_car.price == payload["price"]


@pytest.mark.django_db
def test_delete_car(admin_client, new_car):
    response = admin_client.delete(f"/api/car/{new_car.id}/")
    assert response.status_code == 204
    new_car.refresh_from_db()
    assert new_car.is_active == False


@pytest.mark.django_db
def test_delete_car_403(user_client, new_car):
    response = user_client.delete(f"/api/car/{new_car.id}/")

    assert response.status_code == 403
