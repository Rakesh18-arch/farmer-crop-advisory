def test_market_prices_list(client):
    res = client.get("/api/market/prices")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "prices" in data

def test_market_price_history(client):
    res = client.get("/api/market/history?crop=Cotton&days=10")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "data" in data
    assert data["data"]["crop_name"] == "Cotton"
    assert "history" in data["data"]
    assert len(data["data"]["history"]) > 0

def test_nearby_markets(client):
    res = client.get("/api/market/nearby?district=Kurnool")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "markets" in data
    assert len(data["markets"]) > 0
