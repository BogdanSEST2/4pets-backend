def test_health_check(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.get_json() == {"message": "Main page is working here!!!"}
