from datetime import datetime
from database.db import db

class Disease(db.Model):
    __tablename__ = "diseases"

    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(100), nullable=False, index=True)
    disease_name = db.Column(db.String(150), nullable=False, index=True)
    pathogen_type = db.Column(db.String(50), default="Fungal")  # Fungal, Bacterial, Viral, Pest
    symptoms = db.Column(db.Text, nullable=False)
    treatment = db.Column(db.Text, nullable=False)
    organic_control = db.Column(db.Text, nullable=True)
    chemical_control = db.Column(db.Text, nullable=True)
    prevention_tips = db.Column(db.Text, nullable=True)
    image_sample_url = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "crop_name": self.crop_name,
            "disease_name": self.disease_name,
            "pathogen_type": self.pathogen_type,
            "symptoms": self.symptoms,
            "treatment": self.treatment,
            "organic_control": self.organic_control,
            "chemical_control": self.chemical_control,
            "prevention_tips": self.prevention_tips,
            "image_sample_url": self.image_sample_url
        }

class DiseasePrediction(db.Model):
    __tablename__ = "disease_predictions"

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    image_filename = db.Column(db.String(255), nullable=False)
    detected_crop = db.Column(db.String(100), nullable=False)
    detected_disease = db.Column(db.String(150), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    symptoms = db.Column(db.Text, nullable=True)
    treatment = db.Column(db.Text, nullable=True)
    prevention_tips = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "farmer_id": self.farmer_id,
            "image_filename": self.image_filename,
            "detected_crop": self.detected_crop,
            "detected_disease": self.detected_disease,
            "confidence": round(self.confidence, 2),
            "symptoms": self.symptoms,
            "treatment": self.treatment,
            "prevention_tips": self.prevention_tips,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
