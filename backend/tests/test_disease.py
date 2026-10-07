import io
from PIL import Image

def test_disease_knowledgebase(client):
    res = client.get("/api/disease/knowledgebase")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "diseases" in data

def test_pest_catalog(client):
    res = client.get("/api/disease/pests")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert len(data["pests"]) > 0

def test_pest_advisory_cotton_bollworm(client):
    payload = {
        "crop": "Cotton",
        "growth_stage": "Flowering / Boll Formation",
        "symptom": "Flared square, rosette flowers, bored holes with excreta"
    }
    res = client.post("/api/disease/pest-advisory", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "Pink Bollworm" in data["diagnosed_pest"]
    assert "biological_control" in data
    assert "chemical_control" in data

def test_disease_prediction_image_upload(client):
    # Create a synthetic test leaf image in memory
    img = Image.new("RGB", (224, 224), color=(34, 139, 34))  # Forest green leaf
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="JPEG")
    img_byte_arr.seek(0)

    data = {
        "image": (img_byte_arr, "sample_leaf.jpg")
    }
    res = client.post(
        "/api/disease/predict",
        data=data,
        content_type="multipart/form-data"
    )
    assert res.status_code == 200
    res_data = res.get_json()
    assert res_data["success"] is True
    assert "detected_crop" in res_data
    assert "detected_disease" in res_data
    assert "treatment" in res_data
    assert "confidence_score" in res_data
    assert res_data["confidence_score"] > 0
