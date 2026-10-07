def test_chatbot_weather_query(client):
    res = client.post("/api/chatbot/message", json={"message": "What is the weather and rain forecast?"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["intent"] == "weather"
    assert "Weather" in data["reply"]
    assert "suggestions" in data

def test_chatbot_market_price_query(client):
    res = client.post("/api/chatbot/message", json={"message": "What is the cotton mandi rate?"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["intent"] == "market_price"
    assert "Cotton" in data["reply"]

def test_chatbot_fertilizer_query(client):
    res = client.post("/api/chatbot/message", json={"message": "How much urea fertilizer should I apply?"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["intent"] == "fertilizer"
    assert "Urea" in data["reply"]
