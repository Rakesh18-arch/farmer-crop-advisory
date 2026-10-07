def test_schemes_list(client):
    res = client.get("/api/schemes")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "schemes" in data
    assert len(data["schemes"]) > 0

def test_schemes_state_filtering(client):
    res = client.get("/api/schemes?state=Andhra%20Pradesh")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert len(data["schemes"]) > 0
