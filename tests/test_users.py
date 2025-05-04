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


def test_get_users_empty(client):
    response = client.get('/user/users')
    assert response.status_code == 200
    data = response.get_json()
    assert data == []


def test_get_users_after_registration(client):
    client.post('/auth/register', json={"username": "testuser", "password": "testpass"})
    response = client.get('/user/users')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["username"] == "testuser"


def test_get_users(client):
    user = {"username": "jane", "password": "Password321!"}
    client.post("/auth/register", json=user)

    r = client.get("/user/users")
    data = r.get_json()
    assert r.status_code == 200
    assert any(u["username"] == "jane" for u in data)



def test_register_and_login_and_get_me(client):
    user_data = {
        "username": "newuser",
        "password": "NewUserPassword123!"
    }

    register_response = client.post("/auth/register", json=user_data)
    assert register_response.status_code == 201
    reg_json = register_response.get_json()
    assert reg_json["status"] == "success"
    assert "Регистрация успешна" in reg_json["message"]

    login_response = client.post("/auth/login", json=user_data)
    assert login_response.status_code == 200
    login_json = login_response.get_json()
    assert login_json["status"] == "success"
    assert "token" in login_json["data"]
    token = login_json["data"]["token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }
    me_response = client.get("/auth/me", headers=headers)
    assert me_response.status_code == 200
    me_json = me_response.get_json()
    assert me_json["data"]["username"] == "newuser"

    no_auth_response = client.get("/auth/me")
    assert no_auth_response.status_code in [401, 403]
