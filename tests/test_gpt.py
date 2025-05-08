def get_auth_token(client):
    user = {"username": "testuser", "password": "Test1234!"}
    client.post("/auth/register", json=user)
    res = client.post("/auth/login", json=user)
    return res.get_json()["data"]["token"]


def test_gpt_valid_request(client):
    token = get_auth_token(client)
    payload = {"message": "Скажи как пройти в библиотеку?"}
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/gpt/ask", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert "библиотек" in data["response"].lower()


def test_gpt_missing_message(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/gpt/ask", json={}, headers=headers)
    json_data = response.get_json()

    assert response.status_code == 400
    assert json_data["status"] == "error"
    assert "Сообщение отсутствует" in json_data["message"]

