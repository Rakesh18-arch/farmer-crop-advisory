def test_current_weather_endpoint(client):
    res = client.get("/api/weather/current?location=Guntur,Andhra%20Pradesh")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "temperature" in data
    assert "humidity" in data
    assert "condition" in data
    assert "forecast_5_days" in data
    assert "farming_alerts" in data
    assert len(data["forecast_5_days"]) > 0

def test_weather_forecast_endpoint(client):
    res = client.get("/api/weather/forecast")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "forecast" in data

def test_weather_alerts_endpoint(client):
    res = client.get("/api/weather/alerts")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "alerts" in data
