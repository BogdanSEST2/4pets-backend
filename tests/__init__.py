
import pytest
from app import create_app, db



@pytest.fixture
def app():
    app = create_app('testing')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def register_user(client, username="testuser", password="Test1234"):
    return client.post("/auth/register", json={"username": username, "password": password})


def login_user(client, username="testuser", password="Test1234"):
    return client.post("/auth/login", json={"username": username, "password": password})


def test_full_pet_flow(client):
    reg = register_user(client)
    assert reg.status_code == 201

    login = login_user(client)
    assert login.status_code == 200
    token = login.get_json()["data"]["token"]
    headers = {"Authorization": f"Bearer {token}"}

    pets_to_add = [
        {"name": "Барсик", "type": "Кот", "age": 3},
        {"name": "Тузик", "type": "Пёс", "age": 5}
    ]
    for pet in pets_to_add:
        res = client.post("/pet/pets", json={"owner_id": 1, "pet": pet}, headers=headers)
        assert res.status_code == 201

    res = client.get("/pet/pets")
    data = res.get_json()
    assert res.status_code == 200
    assert len(data["pets"]) == 2

    res = client.get("/pet/owner/1")
    data = res.get_json()
    assert res.status_code == 200
    assert len(data["pets"]) == 2

    res = client.delete("/pet/owner/1")
    assert res.status_code == 200

    res = client.get("/pet/owner/1")
    data = res.get_json()
    assert res.status_code == 200
    assert data["pets"] == []
