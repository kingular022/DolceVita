from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_category():
    response = client.post(
        "/categories/?category_name=odziez",
    )
    assert response.status_code == 200
    assert response.json()['name'] == "odziez"
    assert type(response.json()['id']) is int
    print(response.json())


def test_create_invalid_item():
    response = client.post(
        "/items/?item_name=ab&item_description=bawelniana"
        "&item_price=100&item_quantity=20&category_id=2"
    )
    assert response.text == '"Zostały podane nieprawidłowe dane"'
    print(response.json())


def test_create_item_fake_brand():
    response = client.post(
        "/items/?item_name=koszulka&item_description=bawelniana"
        "&item_price=100&item_quantity=20&brand_id=999"
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Brand not found"}
    print(response.json())
