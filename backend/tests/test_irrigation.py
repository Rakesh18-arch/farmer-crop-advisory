def test_irrigation_high_rain_avoidance(client):
    payload = {
        "crop_name": "Cotton",
        "soil_type": "Black",
        "soil_moisture": 30.0,
        "temperature": 28.0,
        "humidity": 85.0,
        "rainfall_forecast": 35.0,  # Heavy rainfall
        "current_weather": "Rainy",
        "growth_stage": "Vegetative"
    }
    res = client.post("/api/irrigation/recommend", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    # Should avoid irrigation due to heavy rainfall forecast
    assert data["irrigation_required"] is False
    assert "SUSPENDED" in data["explanation"]

def test_irrigation_low_moisture_urgent(client):
    payload = {
        "crop_name": "Wheat",
        "soil_type": "Sandy",
        "soil_moisture": 22.0,  # Critically low moisture
        "temperature": 32.0,
        "humidity": 40.0,
        "rainfall_forecast": 0.0,
        "current_weather": "Clear",
        "growth_stage": "Flowering"
    }
    res = client.post("/api/irrigation/recommend", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["irrigation_required"] is True
    assert data["priority"] == "HIGH"
    assert data["water_requirement_estimate_liters"] > 0
