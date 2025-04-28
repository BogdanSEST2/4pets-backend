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


