import pytest

from dealership import models


@pytest.fixture
def fort_brand():
    return models.Brand.objects.create(name="Fort")


@pytest.mark.django_db
def test_create_brand(admin_client):
    payload = {"name": "Ford"}
    response = admin_client.post("/api/brand/", payload)
    assert response.status_code == 201

    data = response.data
    status_from_db = models.Brand.objects.all().first()

    assert data["name"] == status_from_db.name

    response = admin_client.post("/api/brand/", payload)
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_brand_403(user_client):
    payload = {
        "name": "Chevrolet"
    }

    response = user_client.post("/api/brand/", payload)

    assert response.status_code == 403


@pytest.mark.django_db
def test_get_brands(user_client):
    models.Brand.objects.create(name="Chevrolet")
    models.Brand.objects.create(name="Ford")
    response = user_client.get(f"/api/brand/")
    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_update_brand(admin_client, fort_brand):
    payload = {
        "name": "Ford"
    }

    response = admin_client.put(f"/api/brand/{fort_brand.id}/", payload)

    assert response.status_code == 200

    fort_brand.refresh_from_db()

    assert fort_brand.name == "Ford"


@pytest.mark.django_db
def test_update_brand_403(user_client):
    brand = models.Brand.objects.create(name="Fort")

    payload = {
        "name": "Ford"
    }

    response = user_client.put(f"/api/brand/{brand.id}/", payload)

    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_brand(admin_client, ford_brand):
    response = admin_client.delete(f"/api/brand/{ford_brand.id}/")
    assert response.status_code == 204
    ford_brand.refresh_from_db()
    assert ford_brand.is_active == False


@pytest.mark.django_db
def test_delete_brand_403(user_client, ford_brand):
    response = user_client.delete(f"/api/brand/{ford_brand.id}/")

    assert response.status_code == 403
