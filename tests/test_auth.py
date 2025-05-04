import pytest
from app.models.user import User
from app.extensions import db
from app.utils.response import error_response




@pytest.fixture
def user_data():
    return {
        "username": "testuser",
        "password": "TestPassword123!"
    }


def test_register_user(client, user_data):
    response = client.post('/auth/register', json=user_data)
    json_data = response.get_json()

    assert response.status_code == 201
    assert json_data["status"] == "success"
    assert json_data["message"] == "Регистрация успешна"


def test_register_existing_user(client, user_data):
    client.post('/auth/register', json=user_data)
    response = client.post('/auth/register', json=user_data)
    json_data = response.get_json()

    assert response.status_code == 409
    assert json_data["status"] == "error"
    assert json_data["message"] == "Пользователь уже существует"



def test_login_user(client, user_data):
    client.post('/auth/register', json=user_data)
    response = client.post('/auth/login', json=user_data)
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["status"] == "success"
    assert "token" in json_data["data"]


def test_login_invalid_credentials(client):
    response = client.post('/auth/login', json={
        "username": "wronguser",
        "password": "wrongpassword"
    })
    json_data = response.get_json()

    assert response.status_code == 401
    assert json_data["status"] == "error"


def test_register_and_login(client):
    user = {"username": "john", "password": "Secret123!"}
    r1 = client.post("/auth/register", json=user)
    assert r1.status_code == 201

    r2 = client.post("/auth/login", json=user)
    data = r2.get_json()
    assert r2.status_code == 200
    assert "token" in data["data"]
