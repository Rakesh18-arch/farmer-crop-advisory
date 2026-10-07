from database.db import db
from models.crop import Crop
from models.advisory import FertilizerRecommendation

class FertilizerService:
    @staticmethod
    def calculate_fertilizer_advisory(crop_name: str, n: float, p: float, k: float, 
                                      ph: float = 6.5, soil_type: str = "Loamy", farmer_id=None):
        """
        Evaluates soil NPK against optimal crop requirements and returns
        balanced fertilizer advisory with chemical and organic alternatives.
        """
        crop = Crop.query.filter(Crop.name.ilike(f"%{crop_name}%")).first()

        # Default optimal nutrient standards if crop not found in DB
        opt_n_min = crop.optimal_n_min if crop else 80.0
        opt_p_min = crop.optimal_p_min if crop else 40.0
        opt_k_min = crop.optimal_k_min if crop else 40.0

        n_diff = opt_n_min - n
        p_diff = opt_p_min - p
        k_diff = opt_k_min - k

        deficiencies = []
        fertilizers = []
        organic_alternatives = []
        dosage_notes = []

        # Nitrogen Analysis
        if n_diff > 15:
            deficiencies.append("Severe Nitrogen (N) Deficiency")
            fertilizers.append("Urea (46% N) @ 45-55 kg/acre in 2-3 split applications")
            organic_alternatives.append("Well-decomposed Farmyard Manure (FYM) @ 4-5 tonnes/acre or Vermicompost @ 2 tonnes/acre, supplemented with Azotobacter/Rhizobium biofertilizer")
            dosage_notes.append("Top-dress Urea during active vegetative growth; avoid applying during standing water or right before heavy downpours.")
        elif n_diff > 0:
            deficiencies.append("Mild Nitrogen (N) Deficiency")
            fertilizers.append("Urea @ 20-25 kg/acre or Ammonium Sulphate (20.6% N)")
            organic_alternatives.append("Neem-coated compost or groundnut cake @ 200 kg/acre")
            dosage_notes.append("Apply mild top-dressing with irrigation.")

        # Phosphorus Analysis
        if p_diff > 10:
            deficiencies.append("Phosphorus (P) Deficiency")
            fertilizers.append("Di-Ammonium Phosphate (DAP 18:46:0) @ 50 kg/acre or Single Super Phosphate (SSP 16% P2O5) @ 125 kg/acre")
            organic_alternatives.append("Steamed Bone Meal @ 100 kg/acre or Rock Phosphate with Phosphate Solubilizing Bacteria (PSB) culture @ 2 kg/acre")
            dosage_notes.append("Apply complete Phosphorus as basal dose at the time of sowing/transplanting near the root zone.")

        # Potassium Analysis
        if k_diff > 10:
            deficiencies.append("Potassium (K) Deficiency")
            fertilizers.append("Muriate of Potash (MOP 60% K2O) @ 25-30 kg/acre")
            organic_alternatives.append("Wood ash (5-7% K2O) @ 150 kg/acre or fermented banana peel extract / potash-mobilizing bacteria (KMB)")
            dosage_notes.append("Apply Potassium in two splits: 50% basal and 50% at flowering/grain formation stage.")

        # Balanced Status
        if not deficiencies:
            deficiencies.append("Optimal Nutrient Balance")
            fertilizers.append("Maintenance dose: NPK 19:19:19 water-soluble foliar spray @ 5g/L water during flowering.")
            organic_alternatives.append("Apply 2 tonnes/acre compost to maintain soil organic carbon.")
            dosage_notes.append("Soil fertility is currently well-balanced. Avoid superfluous chemical applications.")

        # Soil pH Conditioning Note
        ph_note = ""
        if ph < 6.0:
            ph_note = "Soil is acidic (pH < 6.0). Incorporate Agricultural Lime @ 200-300 kg/acre 2 weeks prior to fertilizer application to unlock nutrient uptake."
        elif ph > 7.8:
            ph_note = "Soil is alkaline (pH > 7.8). Incorporate Agricultural Gypsum @ 250 kg/acre or elemental sulphur with organic matter to neutralize alkalinity."

        precautions = (
            "⚠️ IMPORTANT ADVISORY QUALIFICATION: Recommended dosages are standard regional estimates. "
            "Always calibrate with your local Soil Health Card and Agricultural Extension Officer. "
            "Never mix Urea with unconditioned manure. Wear protective gloves when handling agro-chemicals. "
            + (f" {ph_note}" if ph_note else "")
        )

        deficiency_summary = " & ".join(deficiencies)
        recommended_fert = "; ".join(fertilizers)
        organic_alt = "; ".join(organic_alternatives)
        dosage_plan = "; ".join(dosage_notes)

        # Save advisory record
        new_advisory = FertilizerRecommendation(
            farmer_id=farmer_id,
            crop_name=crop_name,
            deficiency_type=deficiency_summary,
            recommended_fertilizer=recommended_fert,
            dosage_advice=dosage_plan,
            organic_alternative=organic_alt,
            precautions=precautions
        )
        db.session.add(new_advisory)
        db.session.commit()

        return {
            "success": True,
            "crop_name": crop_name,
            "soil_metrics": {"N": n, "P": p, "K": k, "pH": ph, "soil_type": soil_type},
            "nutrient_deficiency": deficiency_summary,
            "recommended_fertilizer": recommended_fert,
            "dosage_advice": dosage_plan,
            "organic_alternative": organic_alt,
            "precautions": precautions,
            "ph_condition_note": ph_note if ph_note else "pH is in the favorable agronomic range."
        }
