def test_fertilizer_advisory_deficiencies(client):
    payload = {
        "crop_name": "Rice",
        "n": 40.0,  # Below optimal (80-120)
        "p": 15.0,  # Below optimal (35-60)
        "k": 10.0,  # Below optimal (35-45)
        "ph": 5.5,  # Acidic
        "soil_type": "Loamy"
    }
    res = client.post("/api/fertilizer/recommend", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "Deficiency" in data["nutrient_deficiency"]
    assert "Urea" in data["recommended_fertilizer"]
    assert "organic_alternative" in data
    assert "precautions" in data
    assert "acidic" in data["ph_condition_note"].lower()

def test_fertilizer_advisory_missing_crop(client):
    res = client.post("/api/fertilizer/recommend", json={"crop_name": ""})
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False
