from datetime import datetime
from database.db import db

class FertilizerRecommendation(db.Model):
    __tablename__ = "fertilizer_recommendations"

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    crop_name = db.Column(db.String(100), nullable=False)
    deficiency_type = db.Column(db.String(150), nullable=False)  # e.g., "Nitrogen Deficiency"
    recommended_fertilizer = db.Column(db.String(200), nullable=False)
    dosage_advice = db.Column(db.Text, nullable=False)
    organic_alternative = db.Column(db.Text, nullable=True)
    precautions = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "farmer_id": self.farmer_id,
            "crop_name": self.crop_name,
            "deficiency_type": self.deficiency_type,
            "recommended_fertilizer": self.recommended_fertilizer,
            "dosage_advice": self.dosage_advice,
            "organic_alternative": self.organic_alternative,
            "precautions": self.precautions,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class IrrigationRecommendation(db.Model):
    __tablename__ = "irrigation_recommendations"

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    crop_name = db.Column(db.String(100), nullable=False)
    irrigation_required = db.Column(db.Boolean, default=True)
    water_req_estimate_liters = db.Column(db.Float, nullable=True)
    priority = db.Column(db.String(20), default="MEDIUM")  # LOW, MEDIUM, HIGH
    recommended_time = db.Column(db.String(100), nullable=True)  # e.g., "Early Morning (6 AM - 8 AM)"
    next_suggested_date = db.Column(db.String(50), nullable=True)
    weather_condition_note = db.Column(db.String(255), nullable=True)
    explanation = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "farmer_id": self.farmer_id,
            "crop_name": self.crop_name,
            "irrigation_required": self.irrigation_required,
            "water_req_estimate_liters": self.water_req_estimate_liters,
            "priority": self.priority,
            "recommended_time": self.recommended_time,
            "next_suggested_date": self.next_suggested_date,
            "weather_condition_note": self.weather_condition_note,
            "explanation": self.explanation,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class WeatherRecord(db.Model):
    __tablename__ = "weather_records"

    id = db.Column(db.Integer, primary_key=True)
    location_query = db.Column(db.String(150), nullable=False, index=True)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    rainfall = db.Column(db.Float, default=0.0)
    wind_speed = db.Column(db.Float, default=0.0)
    condition = db.Column(db.String(100), default="Clear")
    forecast_json = db.Column(db.Text, nullable=True)  # JSON-encoded forecast
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "location_query": self.location_query,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "rainfall": self.rainfall,
            "wind_speed": self.wind_speed,
            "condition": self.condition,
            "forecast_json": self.forecast_json,
            "recorded_at": self.recorded_at.isoformat() if self.recorded_at else None
        }

class GovernmentScheme(db.Model):
    __tablename__ = "government_schemes"

    id = db.Column(db.Integer, primary_key=True)
    scheme_name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    eligibility = db.Column(db.Text, nullable=False)
    benefits = db.Column(db.Text, nullable=False)
    required_documents = db.Column(db.Text, nullable=False)
    application_link = db.Column(db.String(255), nullable=True)
    scheme_type = db.Column(db.String(50), default="Central")  # Central, State
    applicable_state = db.Column(db.String(100), default="All India")
    applicable_crops = db.Column(db.String(255), default="All Crops")
    farmer_category = db.Column(db.String(100), default="Small & Marginal Farmers")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "scheme_name": self.scheme_name,
            "description": self.description,
            "eligibility": self.eligibility,
            "benefits": self.benefits,
            "required_documents": self.required_documents,
            "application_link": self.application_link,
            "scheme_type": self.scheme_type,
            "applicable_state": self.applicable_state,
            "applicable_crops": self.applicable_crops,
            "farmer_category": self.farmer_category,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
