from datetime import datetime
from database.db import db

class Crop(db.Model):
    __tablename__ = "crops"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    category = db.Column(db.String(50), default="Cereal")  # Cereal, Pulse, Commercial, Fruit, Vegetable
    optimal_n_min = db.Column(db.Float, default=60.0)
    optimal_n_max = db.Column(db.Float, default=120.0)
    optimal_p_min = db.Column(db.Float, default=35.0)
    optimal_p_max = db.Column(db.Float, default=60.0)
    optimal_k_min = db.Column(db.Float, default=35.0)
    optimal_k_max = db.Column(db.Float, default=50.0)
    optimal_ph_min = db.Column(db.Float, default=6.0)
    optimal_ph_max = db.Column(db.Float, default=7.5)
    min_rainfall = db.Column(db.Float, default=150.0)  # mm
    max_rainfall = db.Column(db.Float, default=300.0)  # mm
    min_temp = db.Column(db.Float, default=20.0)       # C
    max_temp = db.Column(db.Float, default=35.0)       # C
    season = db.Column(db.String(50), default="Kharif") # Kharif, Rabi, Zaid, Perennial
    growth_duration_days = db.Column(db.Integer, default=120)
    water_requirement = db.Column(db.String(50), default="Medium") # Low, Medium, High
    description = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "optimal_n": f"{self.optimal_n_min} - {self.optimal_n_max}",
            "optimal_p": f"{self.optimal_p_min} - {self.optimal_p_max}",
            "optimal_k": f"{self.optimal_k_min} - {self.optimal_k_max}",
            "optimal_ph": f"{self.optimal_ph_min} - {self.optimal_ph_max}",
            "rainfall_range": f"{self.min_rainfall} - {self.max_rainfall} mm",
            "temp_range": f"{self.min_temp} - {self.max_temp} °C",
            "season": self.season,
            "growth_duration_days": self.growth_duration_days,
            "water_requirement": self.water_requirement,
            "description": self.description
        }

class CropHistory(db.Model):
    __tablename__ = "crop_histories"

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    crop_name = db.Column(db.String(100), nullable=False)
    season = db.Column(db.String(50), nullable=False)  # Kharif, Rabi, Zaid
    year = db.Column(db.Integer, nullable=False)
    yield_achieved = db.Column(db.Float, nullable=True)  # tons or quintals
    area_cultivated = db.Column(db.Float, nullable=True)  # acres
    notes = db.Column(db.String(255), nullable=True)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "farmer_id": self.farmer_id,
            "crop_name": self.crop_name,
            "season": self.season,
            "year": self.year,
            "yield_achieved": self.yield_achieved,
            "area_cultivated": self.area_cultivated,
            "notes": self.notes,
            "recorded_at": self.recorded_at.isoformat() if self.recorded_at else None
        }

class CropRecommendation(db.Model):
    __tablename__ = "crop_recommendations"

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    recommended_crop = db.Column(db.String(100), nullable=False)
    confidence_score = db.Column(db.Float, nullable=False)
    alternative_crop_1 = db.Column(db.String(100), nullable=True)
    alternative_crop_2 = db.Column(db.String(100), nullable=True)
    explanation = db.Column(db.Text, nullable=False)

    # Input telemetry
    input_n = db.Column(db.Float, nullable=False)
    input_p = db.Column(db.Float, nullable=False)
    input_k = db.Column(db.Float, nullable=False)
    input_ph = db.Column(db.Float, nullable=False)
    input_temp = db.Column(db.Float, nullable=False)
    input_humidity = db.Column(db.Float, nullable=False)
    input_rainfall = db.Column(db.Float, nullable=False)
    soil_type = db.Column(db.String(50), nullable=True)
    season = db.Column(db.String(50), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "farmer_id": self.farmer_id,
            "recommended_crop": self.recommended_crop,
            "confidence_score": round(self.confidence_score, 2),
            "alternative_crop_1": self.alternative_crop_1,
            "alternative_crop_2": self.alternative_crop_2,
            "explanation": self.explanation,
            "inputs": {
                "n": self.input_n,
                "p": self.input_p,
                "k": self.input_k,
                "ph": self.input_ph,
                "temperature": self.input_temp,
                "humidity": self.input_humidity,
                "rainfall": self.input_rainfall,
                "soil_type": self.soil_type,
                "season": self.season
            },
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
