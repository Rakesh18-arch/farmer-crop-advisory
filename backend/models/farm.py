from datetime import datetime
from database.db import db

class FarmerProfile(db.Model):
    __tablename__ = "farmer_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    farm_size = db.Column(db.Float, default=2.0)  # acres
    farm_location = db.Column(db.String(255), nullable=True)  # Village / Geo coordinates
    soil_type = db.Column(db.String(50), default="Loamy")  # Alluvial, Black, Red, Sandy, Clay, Loamy
    
    # Soil nutrient values
    n_value = db.Column(db.Float, default=90.0)  # Nitrogen (kg/ha)
    p_value = db.Column(db.Float, default=42.0)  # Phosphorus (kg/ha)
    k_value = db.Column(db.Float, default=43.0)  # Potassium (kg/ha)
    soil_ph = db.Column(db.Float, default=6.5)   # pH (0 - 14)
    soil_moisture = db.Column(db.Float, default=45.0)  # Percentage (%)

    water_source = db.Column(db.String(100), default="Borewell")  # Borewell, Canal, Rainfed, Well, River
    irrigation_type = db.Column(db.String(100), default="Drip Irrigation")  # Drip, Sprinkler, Flood, Furrow
    current_crop = db.Column(db.String(100), default="Rice")
    previous_crops = db.Column(db.String(255), default="Cotton, Groundnut")  # comma-separated

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    farms = db.relationship("Farm", backref="profile", lazy=True, cascade="all, delete-orphan")
    soil_records = db.relationship("SoilRecord", backref="profile", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "farm_size": self.farm_size,
            "farm_location": self.farm_location,
            "soil_type": self.soil_type,
            "n_value": self.n_value,
            "p_value": self.p_value,
            "k_value": self.k_value,
            "soil_ph": self.soil_ph,
            "soil_moisture": self.soil_moisture,
            "water_source": self.water_source,
            "irrigation_type": self.irrigation_type,
            "current_crop": self.current_crop,
            "previous_crops": self.previous_crops,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class Farm(db.Model):
    __tablename__ = "farms"

    id = db.Column(db.Integer, primary_key=True)
    farmer_profile_id = db.Column(db.Integer, db.ForeignKey("farmer_profiles.id"), nullable=False)
    plot_name = db.Column(db.String(100), nullable=False)
    area_acres = db.Column(db.Float, nullable=False)
    survey_number = db.Column(db.String(50), nullable=True)
    soil_type = db.Column(db.String(50), default="Loamy")
    irrigation_source = db.Column(db.String(100), default="Borewell")

    def to_dict(self):
        return {
            "id": self.id,
            "farmer_profile_id": self.farmer_profile_id,
            "plot_name": self.plot_name,
            "area_acres": self.area_acres,
            "survey_number": self.survey_number,
            "soil_type": self.soil_type,
            "irrigation_source": self.irrigation_source
        }

class SoilRecord(db.Model):
    __tablename__ = "soil_records"

    id = db.Column(db.Integer, primary_key=True)
    farmer_profile_id = db.Column(db.Integer, db.ForeignKey("farmer_profiles.id"), nullable=False)
    n = db.Column(db.Float, nullable=False)
    p = db.Column(db.Float, nullable=False)
    k = db.Column(db.Float, nullable=False)
    ph = db.Column(db.Float, nullable=False)
    moisture = db.Column(db.Float, nullable=False)
    organic_carbon = db.Column(db.Float, default=0.5)  # % organic carbon
    notes = db.Column(db.String(255), nullable=True)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "farmer_profile_id": self.farmer_profile_id,
            "n": self.n,
            "p": self.p,
            "k": self.k,
            "ph": self.ph,
            "moisture": self.moisture,
            "organic_carbon": self.organic_carbon,
            "notes": self.notes,
            "recorded_at": self.recorded_at.isoformat() if self.recorded_at else None
        }
