import pytest
from app import create_app, db



@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_get_pets_empty(client):
    response = client.get('/pet/pets')
    assert response.status_code == 200
    data = response.get_json()
    assert data == {"pets": []}


def test_add_pet(client):
    pet_data = {
        "owner_id": 1,
        "pet": {
            "name": "Барсик",
            "type": "Кот",
            "age": 3
        }
    }
    response = client.post('/pet/pets', json=pet_data)
    assert response.status_code == 201
    data = response.get_json()
    assert "Питомец добавлен для владельца" in data["message"]


def test_add_and_get_pets(client):
    user = {"username": "max", "password": "12345Qwe!"}
    client.post("/auth/register", json=user)
    client.post("/auth/login", json=user)

    pet_data = {
        "owner_id": 1,
        "pet": {
            "name": "Шарик",
            "type": "Собака",
            "age": 5
        }
    }
    r1 = client.post("/pet/pets", json=pet_data)
    assert r1.status_code == 201

    r2 = client.get("/pet/pets")
    pets = r2.get_json()["pets"]
    assert len(pets) >= 1
    assert any(p["name"] == "Шарик" for p in pets)


def test_get_pets_by_owner(client):
    pet_data = {
        "owner_id": 1,
        "pet": {
            "name": "Мурзик",
            "type": "Кот",
            "age": 3
        }
    }
    client.post("/pet/pets", json=pet_data)
    r = client.get("/pet/owner/1")
    data = r.get_json()
    assert r.status_code == 200
    assert all(p["owner_id"] == 1 for p in data["pets"])


def test_delete_pet_by_id(client):
    pet_data = {
        "owner_id": 1,
        "pet": {
            "name": "Кеша",
            "type": "Попугай",
            "age": 2
        }
    }
    client.post("/pet/pets", json=pet_data)

    r = client.delete("/pet/pets/1")
    assert r.status_code in [200, 404]


def test_delete_all_pets_by_owner(client):
    owner_id = 1
    pets = [
        {"owner_id": owner_id, "pet": {"name": "Кот", "type": "Кот", "age": 3}},
        {"owner_id": owner_id, "pet": {"name": "Собака", "type": "Собака", "age": 5}}
    ]
    for pet in pets:
        client.post("/pet/pets", json=pet)

    r = client.delete(f"/pet/owner/{owner_id}")
    assert r.status_code == 200
    assert "удалены" in r.get_json()["message"]

    get_response = client.get(f"/pet/owner/{owner_id}")
    assert get_response.status_code == 200
    assert get_response.get_json()["pets"] == []


def test_update_pet(client):
    client.post("/pet/pets", json={
        "owner_id": 1,
        "pet": {"name": "Старый", "type": "Кот", "age": 3}
    })

    get_response = client.get("/pet/pets")
    pet_id = get_response.get_json()["pets"][0]["id"]

    response = client.put(f"/pet/pets/{pet_id}", json={
        "name": "Обновлённый",
        "type": "Котейка",
        "age": 5
    })

    assert response.status_code == 200
    assert "обновлён" in response.get_json()["message"].lower()
