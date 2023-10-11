import pytest
from dealership import models


@pytest.mark.django_db
@pytest.mark.parametrize("name,drivetrain,expected_status",
                         [("Mustang", "FWD", 201), ("Focus", "ABC", 400)])
def test_create_model(admin_client, ford_brand, name,
                      drivetrain, expected_status):
    payload = {
        "name": name,
        "brand": ford_brand.id,
        "drivetrain": drivetrain,
        "engine": "Diesel",
        "bodytype": "Hatchback",
        "transmission": "Automatic"
    }

    response = admin_client.post("/api/model/", payload)
    assert response.status_code == expected_status


@pytest.mark.django_db
def test_create_model_403(user_client, ford_brand):
    payload = {
        "name": "Focus",
        "brand": ford_brand.id,
        "drivetrain": "AWD",
        "engine": "Diesel",
        "bodytype": "Hatchback",
        "transmission": "Automatic"
    }

    response = user_client.post("/api/model/", payload)
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_models(user_client, ford_brand):
    models.Model.objects.create(name="Mustang", brand=ford_brand, drivetrain="AWD", engine="Diesel",
                                bodytype="Hatchback", transmission="Automatic")
    models.Model.objects.create(name="Focus", brand=ford_brand, drivetrain="FWD", engine="Diesel", bodytype="Hatchback",
                                transmission="Automatic")
    response = user_client.get(f"/api/model/")
    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_update_model(admin_client, mustang_model):
    payload = {
        "name": mustang_model.name,
        "brand": mustang_model.brand.id,
        "drivetrain": "FWD",
        "engine": mustang_model.engine,
        "bodytype": mustang_model.bodytype,
        "transmission": mustang_model.transmission
    }

    response = admin_client.put(f"/api/model/{mustang_model.id}/", payload)

    assert response.status_code == 200

    mustang_model.refresh_from_db()

    assert mustang_model.drivetrain == "FWD"


@pytest.mark.django_db
def test_update_model_403(user_client, mustang_model):
    payload = {
        "name": mustang_model.name,
        "brand": mustang_model.brand.id,
        "drivetrain": "FWD",
        "engine": mustang_model.engine,
        "bodytype": mustang_model.bodytype,
        "transmission": mustang_model.transmission
    }

    response = user_client.put(f"/api/model/{mustang_model.id}/", payload)

    assert response.status_code == 403


#
@pytest.mark.django_db
def test_delete_model(admin_client, mustang_model):
    response = admin_client.delete(f"/api/model/{mustang_model.id}/")
    assert response.status_code == 204
    mustang_model.refresh_from_db()
    assert mustang_model.is_active == False


@pytest.mark.django_db
def test_delete_model_403(user_client, mustang_model):
    response = user_client.delete(f"/api/brand/{mustang_model.id}/")
    assert response.status_code == 403
