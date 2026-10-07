import os
import sys

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime, date, timedelta
from app import create_app
from database.db import db
from models.user import User
from models.farm import FarmerProfile, Farm, SoilRecord
from models.crop import Crop, CropHistory
from models.disease import Disease
from models.market import Market, MarketPrice
from models.advisory import GovernmentScheme
from models.notification import Notification

def seed_database():
    app = create_app()
    with app.app_context():
        print("[SEED] Starting database seeding...")
        db.create_all()

        # 1. Seed Admin User
        admin = User.query.filter_by(email="admin@farmeradvisory.org").first()
        if not admin:
            admin = User(
                full_name="Agronomy System Administrator",
                phone_number="9876543210",
                email="admin@farmeradvisory.org",
                preferred_language="en",
                state="Andhra Pradesh",
                district="Guntur",
                village="Agricultural Research Hub",
                role="admin"
            )
            admin.set_password("Admin@123")
            db.session.add(admin)
            print("  Created admin: admin@farmeradvisory.org (Admin@123)")

        # 2. Seed Sample Farmer User
        demo_farmer = User.query.filter_by(email="farmer@demo.org").first()
        if not demo_farmer:
            demo_farmer = User(
                full_name="Ramesh Kumar",
                phone_number="9123456780",
                email="farmer@demo.org",
                preferred_language="en",
                state="Andhra Pradesh",
                district="Kurnool",
                village="Nandyal",
                role="farmer"
            )
            demo_farmer.set_password("Farmer@123")
            db.session.add(demo_farmer)
            db.session.flush()

            # Profile for demo farmer
            profile = FarmerProfile(
                user_id=demo_farmer.id,
                farm_size=3.5,
                farm_location="Nandyal, Kurnool District (15.4764° N, 78.4832° E)",
                soil_type="Black",
                n_value=85.0,
                p_value=45.0,
                k_value=42.0,
                soil_ph=6.8,
                soil_moisture=48.0,
                water_source="Borewell & Canal",
                irrigation_type="Drip Irrigation",
                current_crop="Cotton",
                previous_crops="Groundnut, Bengal Gram"
            )
            db.session.add(profile)
            db.session.flush()

            # Initial Farm Plot
            plot = Farm(
                farmer_profile_id=profile.id,
                plot_name="North Field Plot A",
                area_acres=3.5,
                survey_number="SY-104/2B",
                soil_type="Black",
                irrigation_source="Borewell"
            )
            db.session.add(plot)

            # Crop History records
            hist1 = CropHistory(
                farmer_id=demo_farmer.id,
                crop_name="Groundnut",
                season="Kharif",
                year=2024,
                yield_achieved=1.8,
                area_cultivated=3.0,
                notes="Good pod formation, adequate rainfall during pod filling."
            )
            hist2 = CropHistory(
                farmer_id=demo_farmer.id,
                crop_name="Bengal Gram",
                season="Rabi",
                year=2023,
                yield_achieved=1.4,
                area_cultivated=3.5,
                notes="Standard yield; treated with Trichoderma for wilt prevention."
            )
            db.session.add_all([hist1, hist2])

            # Sample Initial Notifications
            n1 = Notification(
                user_id=demo_farmer.id,
                title="Monsoon Sowing Advisory",
                message="Ideal soil moisture detected for Cotton germination. Plan pre-sowing weed management.",
                category="IRRIGATION",
                priority="MEDIUM"
            )
            n2 = Notification(
                user_id=demo_farmer.id,
                title="Weather Alert: Moderate Rainfall",
                message="Scattered rainfall (15-25mm) forecasted over the next 48 hours. Postpone chemical sprayings.",
                category="WEATHER",
                priority="HIGH"
            )
            db.session.add_all([n1, n2])
            print("  Created demo farmer: farmer@demo.org (Farmer@123)")

        # 3. Seed Comprehensive Crops
        crops_data = [
            {"name": "Rice", "category": "Cereal", "optimal_n_min": 80, "optimal_n_max": 120, "optimal_p_min": 35, "optimal_p_max": 60, "optimal_k_min": 35, "optimal_k_max": 45, "optimal_ph_min": 5.5, "optimal_ph_max": 7.2, "min_rainfall": 200, "max_rainfall": 300, "min_temp": 20, "max_temp": 35, "season": "Kharif", "growth_duration_days": 130, "water_requirement": "High", "description": "Staple food crop; thrives in high temperature, high humidity, and prolonged standing water."},
            {"name": "Wheat", "category": "Cereal", "optimal_n_min": 100, "optimal_n_max": 140, "optimal_p_min": 50, "optimal_p_max": 70, "optimal_k_min": 30, "optimal_k_max": 40, "optimal_ph_min": 6.0, "optimal_ph_max": 7.5, "min_rainfall": 75, "max_rainfall": 150, "min_temp": 12, "max_temp": 25, "season": "Rabi", "growth_duration_days": 120, "water_requirement": "Medium", "description": "Major Rabi grain crop requiring cool growing weather and bright sunshine at ripening."},
            {"name": "Maize", "category": "Cereal", "optimal_n_min": 70, "optimal_n_max": 100, "optimal_p_min": 40, "optimal_p_max": 60, "optimal_k_min": 15, "optimal_k_max": 25, "optimal_ph_min": 5.8, "optimal_ph_max": 7.0, "min_rainfall": 60, "max_rainfall": 120, "min_temp": 18, "max_temp": 32, "season": "Kharif", "growth_duration_days": 100, "water_requirement": "Medium", "description": "Versatile cereal crop used for grain, fodder, and industrial processing. Sensitive to waterlogging."},
            {"name": "Cotton", "category": "Commercial", "optimal_n_min": 100, "optimal_n_max": 140, "optimal_p_min": 35, "optimal_p_max": 60, "optimal_k_min": 15, "optimal_k_max": 30, "optimal_ph_min": 6.0, "optimal_ph_max": 8.0, "min_rainfall": 60, "max_rainfall": 110, "min_temp": 22, "max_temp": 35, "season": "Kharif", "growth_duration_days": 160, "water_requirement": "Medium", "description": "Cash crop requiring deep fertile black soil, warm climate, and moderate rainfall or canal irrigation."},
            {"name": "Groundnut", "category": "Pulse", "optimal_n_min": 15, "optimal_n_max": 30, "optimal_p_min": 40, "optimal_p_max": 65, "optimal_k_min": 30, "optimal_k_max": 45, "optimal_ph_min": 6.0, "optimal_ph_max": 7.2, "min_rainfall": 50, "max_rainfall": 100, "min_temp": 22, "max_temp": 32, "season": "Kharif", "growth_duration_days": 110, "water_requirement": "Medium", "description": "Leguminous oilseed crop that enriches soil through biological nitrogen fixation."},
            {"name": "Sugarcane", "category": "Commercial", "optimal_n_min": 150, "optimal_n_max": 250, "optimal_p_min": 60, "optimal_p_max": 90, "optimal_k_min": 80, "optimal_k_max": 120, "optimal_ph_min": 6.5, "optimal_ph_max": 8.0, "min_rainfall": 150, "max_rainfall": 250, "min_temp": 20, "max_temp": 38, "season": "Perennial", "growth_duration_days": 365, "water_requirement": "High", "description": "Long duration tropical cash crop with heavy nutrient demand and continuous water availability need."},
            {"name": "Millet", "category": "Cereal", "optimal_n_min": 40, "optimal_n_max": 60, "optimal_p_min": 20, "optimal_p_max": 40, "optimal_k_min": 15, "optimal_k_max": 25, "optimal_ph_min": 5.5, "optimal_ph_max": 7.5, "min_rainfall": 35, "max_rainfall": 75, "min_temp": 25, "max_temp": 38, "season": "Kharif", "growth_duration_days": 90, "water_requirement": "Low", "description": "Climate-resilient nutri-cereal requiring minimal water; ideal for arid and semi-arid tracts."},
            {"name": "Pulses (Chickpea/Bengal Gram)", "category": "Pulse", "optimal_n_min": 20, "optimal_n_max": 40, "optimal_p_min": 50, "optimal_p_max": 70, "optimal_k_min": 60, "optimal_k_max": 80, "optimal_ph_min": 6.0, "optimal_ph_max": 8.0, "min_rainfall": 40, "max_rainfall": 90, "min_temp": 15, "max_temp": 28, "season": "Rabi", "growth_duration_days": 105, "water_requirement": "Low", "description": "High-protein pulse crop that requires mild winters and well-drained loam or clay soils."},
            {"name": "Tomato", "category": "Vegetable", "optimal_n_min": 80, "optimal_n_max": 120, "optimal_p_min": 60, "optimal_p_max": 90, "optimal_k_min": 60, "optimal_k_max": 100, "optimal_ph_min": 6.0, "optimal_ph_max": 7.0, "min_rainfall": 60, "max_rainfall": 120, "min_temp": 18, "max_temp": 30, "season": "Rabi", "growth_duration_days": 100, "water_requirement": "Medium", "description": "High-value commercial horticultural crop with high potassium and phosphorus demand."},
            {"name": "Chilli", "category": "Vegetable", "optimal_n_min": 90, "optimal_n_max": 130, "optimal_p_min": 45, "optimal_p_max": 70, "optimal_k_min": 45, "optimal_k_max": 70, "optimal_ph_min": 6.0, "optimal_ph_max": 7.5, "min_rainfall": 50, "max_rainfall": 100, "min_temp": 20, "max_temp": 35, "season": "Kharif", "growth_duration_days": 140, "water_requirement": "Medium", "description": "Pungent spice crop requiring warm and humid climate during early growth and dry weather at maturity."},
            {"name": "Soybean", "category": "Pulse", "optimal_n_min": 20, "optimal_n_max": 40, "optimal_p_min": 60, "optimal_p_max": 80, "optimal_k_min": 35, "optimal_k_max": 50, "optimal_ph_min": 6.0, "optimal_ph_max": 7.5, "min_rainfall": 70, "max_rainfall": 130, "min_temp": 20, "max_temp": 32, "season": "Kharif", "growth_duration_days": 105, "water_requirement": "Medium", "description": "Dual oilseed and protein crop fixing substantial atmospheric nitrogen."},
            {"name": "Banana", "category": "Fruit", "optimal_n_min": 150, "optimal_n_max": 220, "optimal_p_min": 50, "optimal_p_max": 80, "optimal_k_min": 150, "optimal_k_max": 250, "optimal_ph_min": 6.0, "optimal_ph_max": 7.5, "min_rainfall": 120, "max_rainfall": 220, "min_temp": 22, "max_temp": 35, "season": "Perennial", "growth_duration_days": 330, "water_requirement": "High", "description": "Heavy potassium consumer; requires moist tropical conditions and wind protection."}
        ]
        for c in crops_data:
            if not Crop.query.filter_by(name=c["name"]).first():
                db.session.add(Crop(**c))
        print("  Crops database seeded.")

        # 4. Seed Diseases
        diseases_data = [
            {
                "crop_name": "Tomato",
                "disease_name": "Tomato Early Blight",
                "pathogen_type": "Fungal (Alternaria solani)",
                "symptoms": "Dark brown concentric rings (target board pattern) on older leaves, yellowing halos, stem lesions, premature defoliation.",
                "treatment": "Remove lower infected foliage. Apply Chlorothalonil or Mancozeb fungicide spray at early emergence.",
                "organic_control": "Neem oil spray (3-5 ml/L), Trichoderma viride bio-fungicide, Copper hydroxide spray.",
                "chemical_control": "Mancozeb 75% WP @ 2.5 g/L or Azoxystrobin 23% SC @ 1 ml/L water.",
                "prevention_tips": "Rotate with non-solanaceous crops, avoid overhead sprinkler irrigation, maintain 60cm plant spacing for air circulation."
            },
            {
                "crop_name": "Tomato",
                "disease_name": "Tomato Late Blight",
                "pathogen_type": "Oomycete (Phytophthora infestans)",
                "symptoms": "Irregular dark water-soaked lesions on leaves and stems; white fuzzy mildew on underside during cool damp conditions.",
                "treatment": "Immediately destroy heavily diseased plants. Spray systemic fungicides before rain events.",
                "organic_control": "Bordeaux mixture (1%), Bacillus subtilis bio-formulations.",
                "chemical_control": "Metalaxyl 8% + Mancozeb 64% WP (Ridomil MZ) @ 2.5 g/L water.",
                "prevention_tips": "Select blight-resistant hybrids, destroy cull piles, keep soil mulched with straw."
            },
            {
                "crop_name": "Tomato",
                "disease_name": "Tomato Leaf Mold",
                "pathogen_type": "Fungal (Passalora fulva)",
                "symptoms": "Pale green or yellowish spots on upper leaf surfaces; olive green to brown velvety mold patches underneath.",
                "treatment": "Prune excess branches to improve ventilation and reduce relative humidity below 80%.",
                "organic_control": "Sulfur dusting or bio-pesticide spray during early morning.",
                "chemical_control": "Difenoconazole 25% EC @ 0.5 ml/L water.",
                "prevention_tips": "Ensure greenhouse and polytunnel aeration, drip irrigate exclusively at ground level."
            },
            {
                "crop_name": "Potato",
                "disease_name": "Potato Early Blight",
                "pathogen_type": "Fungal (Alternaria solani)",
                "symptoms": "Small brown spots on leaflets showing concentric rings; dark leathery sunken lesions on tubers.",
                "treatment": "Maintain balanced nitrogen fertility; spray protective contact fungicides.",
                "organic_control": "Pseudomonas fluorescens seed and foliage treatment @ 10 g/L.",
                "chemical_control": "Propineb 70% WP @ 2 g/L or Chlorothalonil 75% WP @ 2 g/L.",
                "prevention_tips": "Plant certified seed tubers, burn diseased stubble post-harvest."
            },
            {
                "crop_name": "Potato",
                "disease_name": "Potato Late Blight",
                "pathogen_type": "Oomycete (Phytophthora infestans)",
                "symptoms": "Rapid brown/black blighting of foliage, foul odor in fields, tuber rot with brownish granular flesh.",
                "treatment": "Urgent spray of translaminar systemic oomyceticide upon first symptomatic leaflet.",
                "organic_control": "Copper oxychloride (Blitox) @ 3 g/L water.",
                "chemical_control": "Cymoxanil 8% + Mancozeb 64% WP @ 2 g/L or Dimethomorph 50% WP @ 1 g/L.",
                "prevention_tips": "Earthing up ridge height to protect tubers from spores washing down from leaves."
            },
            {
                "crop_name": "Rice",
                "disease_name": "Rice Leaf Blast",
                "pathogen_type": "Fungal (Magnaporthe oryzae)",
                "symptoms": "Spindle-shaped elliptical lesions with gray centers and dark brown margins on leaves; neck rot at panicle base.",
                "treatment": "Drain excess standing water temporarily; apply Tricyclazole.",
                "organic_control": "Seed treatment with Pseudomonas fluorescens @ 10 g/kg seed.",
                "chemical_control": "Tricyclazole 75% WP @ 0.6 g/L or Isoprothiolane 40% EC @ 1.5 ml/L water.",
                "prevention_tips": "Avoid excessive nitrogen top-dressing; split urea applications into 3-4 doses."
            },
            {
                "crop_name": "General Crops",
                "disease_name": "Healthy Leaf",
                "pathogen_type": "None (No Disease Detected)",
                "symptoms": "Uniform vibrant green foliage, no necrotic spots, healthy vascular venation.",
                "treatment": "No chemical treatment required. Continue regular agronomic and nutrient management.",
                "organic_control": "Maintain soil organic carbon with compost and vermicompost.",
                "chemical_control": "None required.",
                "prevention_tips": "Monitor crop weekly for early pest threshold counts."
            }
        ]
        for d in diseases_data:
            if not Disease.query.filter_by(disease_name=d["disease_name"]).first():
                db.session.add(Disease(**d))
        print("  Crop diseases database seeded.")

        # 5. Seed Agricultural Markets & Prices
        markets_data = [
            {"name": "Kurnool Agricultural Market Yard", "district": "Kurnool", "state": "Andhra Pradesh", "latitude": 15.8281, "longitude": 78.0373, "contact_number": "08518-220145"},
            {"name": "Guntur Mirchi Yard", "district": "Guntur", "state": "Andhra Pradesh", "latitude": 16.3067, "longitude": 80.4365, "contact_number": "0863-2234567"},
            {"name": "Warangal Enmamula Cotton Market", "district": "Warangal", "state": "Telangana", "latitude": 17.9689, "longitude": 79.5941, "contact_number": "0870-2567890"},
            {"name": "Pune Gultekdi APMC", "district": "Pune", "state": "Maharashtra", "latitude": 18.5204, "longitude": 73.8567, "contact_number": "020-24263001"},
            {"name": "Khanna Grain Market", "district": "Ludhiana", "state": "Punjab", "latitude": 30.7046, "longitude": 76.2163, "contact_number": "01628-223344"}
        ]
        for m in markets_data:
            existing_m = Market.query.filter_by(name=m["name"]).first()
            if not existing_m:
                market_obj = Market(**m)
                db.session.add(market_obj)
                db.session.flush()

                # Seed sample prices
                prices = [
                    {"crop_name": "Cotton", "variety": "Medium Staple", "min_price": 6800, "max_price": 7550, "modal_price": 7250, "price_trend": "UP"},
                    {"crop_name": "Rice", "variety": "Sona Masoori", "min_price": 2800, "max_price": 3450, "modal_price": 3200, "price_trend": "STABLE"},
                    {"crop_name": "Maize", "variety": "Hybrid Yellow", "min_price": 2100, "max_price": 2400, "modal_price": 2250, "price_trend": "UP"},
                    {"crop_name": "Chilli", "variety": "Teja Hot", "min_price": 14000, "max_price": 19500, "modal_price": 17800, "price_trend": "UP"},
                    {"crop_name": "Tomato", "variety": "Hybrid Red", "min_price": 1200, "max_price": 2100, "modal_price": 1650, "price_trend": "DOWN"},
                    {"crop_name": "Groundnut", "variety": "Bold Pod", "min_price": 5900, "max_price": 6600, "modal_price": 6300, "price_trend": "STABLE"}
                ]
                for p in prices:
                    db.session.add(MarketPrice(market_id=market_obj.id, **p))
        print("  APMC Mandi markets & commodity rates seeded.")

        # 6. Seed Premier Government Schemes
        schemes_data = [
            {
                "scheme_name": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
                "description": "Income support scheme of Rs 6,000 per year in three equal installments directly to land-holding farmer families.",
                "eligibility": "All landholding farmer families having cultivable agricultural land up to any size (excluding institutional and income-tax paying entities).",
                "benefits": "Direct Bank Transfer (DBT) of Rs 6,000 annually (Rs 2,000 every 4 months).",
                "required_documents": "Aadhaar Card, Land Record (Pattadar Passbook / ROR-1B), Active Bank Account linked with Aadhaar.",
                "application_link": "https://pmkisan.gov.in",
                "scheme_type": "Central",
                "applicable_state": "All India",
                "applicable_crops": "All Crops",
                "farmer_category": "Small, Marginal & Medium Farmers"
            },
            {
                "scheme_name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
                "description": "Comprehensive yield-based crop insurance coverage against non-preventable natural risks from pre-sowing to post-harvest.",
                "eligibility": "Farmers growing notified crops in notified areas (both loanee and non-loanee farmers).",
                "benefits": "Low premium rate: 2% for Kharif, 1.5% for Rabi food/oilseeds, and 5% for commercial/horticultural crops; 100% loss coverage.",
                "required_documents": "Land record proof, Sowing certificate / Self-declaration, Aadhaar, Bank Passbook copy.",
                "application_link": "https://pmfby.gov.in",
                "scheme_type": "Central",
                "applicable_state": "All India",
                "applicable_crops": "Food grains, Oilseeds, Commercial Crops",
                "farmer_category": "All Farmers"
            },
            {
                "scheme_name": "Soil Health Card Scheme",
                "description": "Government program issuing soil nutrient report cards with tailored fertilizer and micronutrient advisory every 2 years.",
                "eligibility": "All agricultural landowners across all states and union territories.",
                "benefits": "Free laboratory analysis of 12 soil parameters (N, P, K, S, Zn, Fe, Cu, Mn, Bo, pH, EC, OC) with dosage guidelines.",
                "required_documents": "Farmer Identity Proof, Land Survey Number.",
                "application_link": "https://soilhealth.dac.gov.in",
                "scheme_type": "Central",
                "applicable_state": "All India",
                "applicable_crops": "All Crops",
                "farmer_category": "All Farmers"
            },
            {
                "scheme_name": "Rythu Bandhu / Farmer Investment Support Scheme",
                "description": "Agricultural investment support scheme providing direct financial grant to farmers for purchase of seeds, fertilizers, and inputs.",
                "eligibility": "Resident agricultural land-owning farmers in Telangana and Andhra Pradesh.",
                "benefits": "Direct grant of Rs 5,000 to Rs 7,500 per acre per season twice a year.",
                "required_documents": "Pattadar passbook, Aadhaar card, Active bank account details.",
                "application_link": "https://rythubandhu.telangana.gov.in",
                "scheme_type": "State",
                "applicable_state": "Telangana & Andhra Pradesh",
                "applicable_crops": "All Field Crops",
                "farmer_category": "Land-owning Farmers"
            },
            {
                "scheme_name": "Paramparagat Krishi Vikas Yojana (PKVY)",
                "description": "Organic farming promotion through cluster approach and Participatory Guarantee System (PGS) certification.",
                "eligibility": "Farmers willing to mobilize in clusters of 20 or more hectares for chemical-free farming.",
                "benefits": "Financial assistance of Rs 50,000 per hectare for cluster formation, bio-fertilizers, organic inputs, and marketing.",
                "required_documents": "Cluster membership form, Land ownership records, KYC documents.",
                "application_link": "https://pgsindia-ncof.gov.in",
                "scheme_type": "Central",
                "applicable_state": "All India",
                "applicable_crops": "Organic Produce, Millets, Pulses",
                "farmer_category": "Small & Marginal Clusters"
            }
        ]
        for s in schemes_data:
            if not GovernmentScheme.query.filter_by(scheme_name=s["scheme_name"]).first():
                db.session.add(GovernmentScheme(**s))
        print("  Government agricultural welfare schemes seeded.")

        db.session.commit()
        print("[SUCCESS] Database seeding completed successfully!")

if __name__ == "__main__":
    seed_database()
