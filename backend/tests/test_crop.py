def test_crop_list(client):
    res = client.get("/api/crop/list")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "crops" in data

def test_crop_recommendation_heuristic(client):
    payload = {
        "n": 80.0,
        "p": 45.0,
        "k": 40.0,
        "temperature": 24.0,
        "humidity": 80.0,
        "ph": 6.5,
        "rainfall": 220.0,
        "soil_type": "Clay",
        "season": "Kharif"
    }
    res = client.post("/api/crop/recommend", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "recommended_crop" in data
    assert "confidence_score" in data
    assert "explanation" in data
    assert data["confidence_score"] > 0

def test_crop_recommendation_invalid_inputs(client):
    # Invalid pH (> 14)
    payload = {
        "n": 80.0,
        "p": 45.0,
        "k": 40.0,
        "ph": 16.5,
        "temperature": 25.0,
        "humidity": 70.0,
        "rainfall": 100.0
    }
    res = client.post("/api/crop/recommend", json=payload)
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False
