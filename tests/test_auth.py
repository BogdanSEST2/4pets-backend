import pytest
from app import create_app, db
from app.models.user import User




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


def test_register_user(client):
    response = client.post('/auth/register', json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Регистрация успешна"


def test_login_user(client):
    client.post('/auth/register', json={"username": "testuser", "password": "testpass"})
    response = client.post('/auth/login', json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data
