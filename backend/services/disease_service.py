import os
import uuid
from werkzeug.utils import secure_filename
from database.db import db
from models.disease import Disease, DiseasePrediction
from ml.disease_detection.disease_predictor import predict_crop_disease
from utils.validators import allowed_file

class DiseaseService:
    @staticmethod
    def process_and_diagnose_image(file_storage, upload_folder: str, farmer_id: int = None) -> tuple:
        """
        Validates, securely stores, and executes AI disease diagnosis on an uploaded leaf image.
        Enriches diagnosis with database symptoms and treatment protocols.
        """
        if not file_storage or file_storage.filename == "":
            return {"success": False, "message": "No leaf image file was provided."}, 400

        allowed_exts = {"png", "jpg", "jpeg", "webp"}
        if not allowed_file(file_storage.filename, allowed_exts):
            return {
                "success": False,
                "message": f"Unsupported file type. Please upload an image with extension: {', '.join(allowed_exts)}."
            }, 400

        # Generate unique secure filename
        original_name = secure_filename(file_storage.filename)
        ext = original_name.rsplit(".", 1)[1].lower() if "." in original_name else "jpg"
        unique_filename = f"leaf_{uuid.uuid4().hex[:12]}.{ext}"
        save_path = os.path.join(upload_folder, unique_filename)

        os.makedirs(upload_folder, exist_ok=True)
        file_storage.save(save_path)

        # Run diagnosis
        try:
            diag_result = predict_crop_disease(save_path)
        except Exception as e:
            return {
                "success": False,
                "message": f"Image processing failed: {str(e)}. Please try another photo."
            }, 500

        detected_crop = diag_result["detected_crop"]
        detected_disease = diag_result["detected_disease"]
        confidence = diag_result["confidence_score"]

        # Fetch detailed treatment protocols from Disease knowledgebase
        disease_info = Disease.query.filter(
            Disease.disease_name.ilike(f"%{detected_disease}%")
        ).first()

        symptoms = disease_info.symptoms if disease_info else "Visual lesions and discoloration on leaf surface."
        treatment = disease_info.treatment if disease_info else "Isolate infected plants and apply broad-spectrum bio-fungicide."
        organic_control = disease_info.organic_control if disease_info else "Spray 5% Neem Seed Kernel Extract (NSKE) or Trichoderma viride."
        chemical_control = disease_info.chemical_control if disease_info else "Mancozeb 75% WP @ 2g/L water."
        prevention_tips = disease_info.prevention_tips if disease_info else "Maintain clean field sanitation and avoid excessive overhead irrigation."

        # Save to database
        prediction_record = DiseasePrediction(
            farmer_id=farmer_id,
            image_filename=unique_filename,
            detected_crop=detected_crop,
            detected_disease=detected_disease,
            confidence=confidence,
            symptoms=symptoms,
            treatment=treatment,
            prevention_tips=prevention_tips
        )
        db.session.add(prediction_record)
        db.session.commit()

        return {
            "success": True,
            "prediction_id": prediction_record.id,
            "detected_crop": detected_crop,
            "detected_disease": detected_disease,
            "confidence_score": confidence,
            "model_status": diag_result.get("model_status"),
            "image_filename": unique_filename,
            "image_url": f"/api/disease/image/{unique_filename}",
            "symptoms": symptoms,
            "treatment": treatment,
            "organic_control": organic_control,
            "chemical_control": chemical_control,
            "prevention_tips": prevention_tips,
            "image_metrics": diag_result.get("image_metrics")
        }, 200
