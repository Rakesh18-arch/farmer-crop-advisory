import re
import uuid
from database.db import db
from models.chat import ChatMessage
from models.crop import Crop
from models.market import MarketPrice
from models.advisory import GovernmentScheme
from services.weather_service import WeatherService
from services.fertilizer_service import FertilizerService

class ChatbotService:
    """
    Hybrid Agricultural Conversational Engine.
    Combines rule-based NLP intent classification with live platform telemetry
    and database lookups to answer farmers in English, Telugu, and Hindi context.
    """

    INTENT_KEYWORDS = {
        "weather": [
            "weather", "rain", "temperature", "forecast", "climate", "rainfall", "storm",
            "varsham", "havamana", "mausam", "barish", "thufan"
        ],
        "crop_recommendation": [
            "recommend", "which crop", "best crop", "sow", "plant", "cultivate", "crop selection",
            "pandu", "fasal", "bone"
        ],
        "fertilizer": [
            "fertilizer", "urea", "dap", "potash", "npk", "nutrient", "nitrogen", "deficiency",
            "manure", "vermicompost", "eruvulu", "khaad"
        ],
        "irrigation": [
            "irrigation", "water", "watering", "dry soil", "moisture", "drip", "sprinkler",
            "neeru", "paani", "sinchai"
        ],
        "disease": [
            "disease", "blight", "yellow leaves", "spots", "fungus", "mold", "rot", "blast",
            "thegulu", "rog", "bimari"
        ],
        "pest": [
            "pest", "insect", "worm", "caterpillar", "bollworm", "whitefly", "thrips", "borer",
            "keeda", "purugu"
        ],
        "market_price": [
            "price", "rate", "mandi", "market", "bhav", "cost", "apmc", "dharalu", "daam"
        ],
        "government_scheme": [
            "scheme", "subsidy", "pm kisan", "pmfby", "rythu bandhu", "loan", "grant",
            "pathakam", "yojana", "sarkari"
        ],
        "soil_health": [
            "soil", "ph", "alkaline", "acidic", "matti", "mitti", "bhumi"
        ]
    }

    @staticmethod
    def process_message(user_message: str, session_id: str = None, user_id: int = None, language: str = "en", preferred_provider: str = None) -> dict:
        """Parses user query, invokes LLM Agricultural reasoning, and saves interaction."""
        if not user_message or not user_message.strip():
            return {
                "reply": "Please ask a question regarding crops, weather, fertilizer, diseases, or market prices.",
                "intent": "unknown",
                "suggestions": ["What crop should I grow?", "Today's weather", "Cotton mandi price"],
                "provider": "agri-neural",
                "model": "AgriLLM-Neural-v2.6"
            }

        cleaned_text = user_message.lower().strip()
        session_id = session_id or str(uuid.uuid4())

        # 1. Detect intent
        detected_intent = ChatbotService._detect_intent(cleaned_text)

        # 2. Fetch past conversation history if available
        history_records = []
        try:
            prev_msgs = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.created_at.asc()).limit(8).all()
            for m in prev_msgs:
                history_records.append({"sender": m.sender, "message": m.message_text})
        except Exception:
            pass

        # 3. Invoke LLM Service
        from services.llm_service import LLMService
        llm_res = LLMService.generate_response(
            prompt=user_message,
            conversation_history=history_records,
            context={"intent": detected_intent, "language": language},
            preferred_provider=preferred_provider
        )

        reply_text = llm_res.get("text") if llm_res else None
        llm_provider = llm_res.get("provider", "agri-neural") if llm_res else "agri-neural"
        llm_model = llm_res.get("model", "AgriLLM-Neural-v2.6") if llm_res else "AgriLLM-Neural-v2.6"

        # Fallback to rule-based engine if LLM text is empty
        if not reply_text:
            reply_text, suggestions = ChatbotService._generate_response(detected_intent, cleaned_text, language)
        else:
            suggestions = [
                "Recommend best crop for my soil",
                "How to cure leaf blight disease?",
                "Organic fertilizer calculation",
                "Today's APMC Mandi rates"
            ]

        # 4. Log interaction to database
        try:
            user_msg_record = ChatMessage(
                user_id=user_id,
                session_id=session_id,
                sender="user",
                message_text=user_message,
                detected_intent=detected_intent
            )
            bot_msg_record = ChatMessage(
                user_id=user_id,
                session_id=session_id,
                sender="bot",
                message_text=reply_text,
                detected_intent=detected_intent
            )
            db.session.add_all([user_msg_record, bot_msg_record])
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"[WARN] Error saving chat message: {e}")

        return {
            "reply": reply_text,
            "intent": detected_intent,
            "session_id": session_id,
            "suggestions": suggestions,
            "provider": llm_provider,
            "model": llm_model
        }

    @staticmethod
    def _detect_intent(text: str) -> str:
        matched_scores = {}
        for intent, keywords in ChatbotService.INTENT_KEYWORDS.items():
            score = sum(1 for kw in keywords if re.search(rf"\b{kw}\b", text))
            if score > 0:
                matched_scores[intent] = score

        if matched_scores:
            return max(matched_scores, key=matched_scores.get)
        return "general_farming"

    @staticmethod
    def _generate_response(intent: str, text: str, language: str = "en") -> tuple[str, list]:
        """Formulates expert response and context-relevant quick reply suggestions."""
        if intent == "weather":
            weather = WeatherService.get_weather_data()
            reply = (
                f"🌤️ Current Weather in {weather.get('location')}:\n"
                f"• Temperature: {weather.get('temperature')}°C (Feels like {weather.get('feels_like')}°C)\n"
                f"• Humidity: {weather.get('humidity')}%\n"
                f"• Condition: {weather.get('description')}\n"
                f"• Wind: {weather.get('wind_speed_kmh')} km/h\n\n"
                f"💡 Farming Advisory: {weather.get('farming_alerts', [{}])[0].get('message', 'Normal farming operations can continue.')}"
            )
            return reply, ["5-day weather forecast", "Is it good to spray today?", "When to irrigate?"]

        elif intent == "market_price":
            # Search for mentioned crop
            found_crop = "Cotton"
            for c in ["rice", "cotton", "maize", "chilli", "tomato", "wheat", "groundnut"]:
                if c in text:
                    found_crop = c.capitalize()
                    break

            price_record = MarketPrice.query.filter(MarketPrice.crop_name.ilike(f"%{found_crop}%")).first()
            if price_record:
                trend_suffix = " 🔼" if price_record.price_trend == "UP" else ""
                market_name = price_record.market.name if price_record.market else "Regional APMC"
                reply = (
                    f"Market Intelligence for {found_crop}:\n"
                    f"• Market Yard: {market_name}\n"
                    f"• Modal (Average) Price: Rs {price_record.modal_price:,.0f} / Quintal\n"
                    f"• Range: Rs {price_record.min_price:,.0f} - Rs {price_record.max_price:,.0f} / Quintal\n"
                    f"• Trend: {price_record.price_trend}{trend_suffix}\n\n"
                    f"Visit the Market Prices tab for 15-day price forecast charts."
                )
            else:
                reply = f"Currently tracked modal rates across APMC mandis: Cotton (~Rs 7,250/Q), Chilli (~Rs 17,800/Q), Rice (~Rs 3,200/Q)."
            return reply, [f"{found_crop} price history", "Nearby APMC mandis", "Chilli market rate"]

        elif intent == "fertilizer":
            reply = (
                "🧪 Fertilizer & Soil Nutrient Guidelines:\n"
                "• For Nitrogen deficit: Top-dress Urea (46% N) in 2-3 split doses with adequate moisture.\n"
                "• For Phosphorus deficit: Apply DAP (18:46:0) or SSP as a basal dose near the root zone.\n"
                "• For Potassium deficit: Apply MOP (Muriate of Potash 60%) at basal and flowering stages.\n"
                "• Organic Alternative: Supplement with Farmyard Manure (4t/acre) and Vermicompost.\n\n"
                "👉 Use our 'Fertilizer Recommendation' tool to get exact dosage calibrated for your field."
            )
            return reply, ["Fertilizer for Cotton", "Organic pest control", "Soil test analysis"]

        elif intent == "irrigation":
            reply = (
                "💧 Smart Irrigation Advisory:\n"
                "• Avoid irrigating if heavy rainfall (>15mm) is predicted within 48 hours.\n"
                "• Critical watering stages: Flowering, Pod/Boll development, and Grain formation.\n"
                "• Optimal timing: Early Morning (6:00 - 8:30 AM) or Late Evening to minimize evaporative losses.\n"
                "• Drip irrigation saves 40-60% water compared to furrow flooding."
            )
            return reply, ["Irrigation for Rice", "Current soil moisture status", "Weather alert"]

        elif intent == "disease":
            reply = (
                "🍃 Crop Disease Diagnosis:\n"
                "You can upload a photograph of an affected leaf in our 'AI Disease Detection' section!\n"
                "Common issues identified:\n"
                "• Tomato / Potato Early Blight: Dark concentric rings with yellow halo -> Chlorothalonil or Mancozeb spray.\n"
                "• Rice Leaf Blast: Spindle-shaped lesions -> Tricyclazole 75% WP @ 0.6g/L.\n"
                "• Organic protection: Spray Neem Oil (3-5 ml/L) or Trichoderma viride."
            )
            return reply, ["Upload leaf photo", "Tomato early blight cure", "Pest control tips"]

        elif intent == "pest":
            reply = (
                "🐛 Integrated Pest Management (IPM):\n"
                "• Pink Bollworm (Cotton): Install pheromone traps @ 8/acre; spray Emamectin Benzoate 5% SG.\n"
                "• Stem Borer (Rice): Clip seedling tips before transplanting; Cartap Hydrochloride 4G.\n"
                "• Sucking Pests (Whitefly/Thrips): Yellow & Blue sticky traps @ 15/acre; Neem oil 5 ml/L.\n"
                "Visit the Pest Advisory page to select your crop and symptom for instant biological remedies."
            )
            return reply, ["Cotton pest remedies", "Yellow sticky traps", "Fruit borer management"]

        elif intent == "government_scheme":
            schemes = GovernmentScheme.query.limit(3).all()
            scheme_bullets = "\n".join([f"• {s.scheme_name}: {s.benefits[:90]}..." for s in schemes])
            reply = (
                f"🏛️ Key Government Agricultural Welfare Schemes:\n\n{scheme_bullets}\n\n"
                f"Check the 'Government Schemes' section for full eligibility, document checklists, and application links."
            )
            return reply, ["PM-KISAN eligibility", "PMFBY crop insurance", "Rythu Bandhu details"]

        elif intent == "crop_recommendation":
            reply = (
                "🌱 AI Crop Recommendation:\n"
                "Our machine learning model analyzes 7 parameters:\n"
                "Nitrogen, Phosphorus, Potassium, Soil pH, Temperature, Humidity, and Rainfall.\n\n"
                "👉 Open the 'Crop Recommendation' page to run an instant analysis for your farm!"
            )
            return reply, ["Recommend crop for my soil", "Best crops for Kharif", "High profit crops"]

        # Default general farming reply
        reply = (
            "Hello! I am your AI Agricultural Assistant 🌾. I can assist you with:\n"
            "1. AI Crop Recommendations based on soil NPK\n"
            "2. Live Weather and Irrigation Alerts\n"
            "3. Fertilizer Deficit & Organic Dosage\n"
            "4. Plant Disease Diagnosis from photos\n"
            "5. Daily Mandi Market Rates & Trends\n"
            "6. Government Welfare Schemes\n\n"
            "How can I help you today?"
        )
        return reply, ["What crop should I grow?", "Today's weather", "Cotton mandi price", "Govt schemes"]
