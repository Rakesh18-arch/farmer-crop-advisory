from datetime import datetime, timedelta
from database.db import db
from models.advisory import IrrigationRecommendation
from models.crop import Crop

class IrrigationService:
    @staticmethod
    def calculate_irrigation_advisory(crop_name: str, soil_type: str, soil_moisture: float,
                                      temperature: float, humidity: float, rainfall_forecast: float,
                                      current_weather: str = "Clear", growth_stage: str = "Vegetative",
                                      farmer_id=None):
        """
        Determines intelligent irrigation scheduling incorporating crop stage,
        field soil moisture, evapotranspiration indicators, and upcoming rain probability.
        """
        crop = Crop.query.filter(Crop.name.ilike(f"%{crop_name}%")).first()
        water_req_level = crop.water_requirement.lower() if crop else "medium"

        # Water retention factors by soil type
        soil_retention = {
            "Sandy": 0.7,   # Drains fast, low moisture capacity
            "Loamy": 1.0,   # Ideal balance
            "Black": 1.3,   # High clay content, high water holding capacity
            "Clay": 1.4,    # Holds water very long, danger of logging
            "Alluvial": 1.1,
            "Red": 0.9
        }.get(soil_type, 1.0)

        # Stage water multiplier
        stage_factor = {
            "Germination": 0.8,
            "Vegetative": 1.1,
            "Flowering": 1.4,       # Critical water need
            "Grain Formation": 1.3, # Critical water need
            "Maturity / Harvesting": 0.5
        }.get(growth_stage, 1.0)

        # Base requirement in liters/acre/day
        base_liters = 15000 if water_req_level == "high" else (10000 if water_req_level == "medium" else 6500)
        daily_req = base_liters * stage_factor * (1.2 if temperature > 32 else 1.0)

        # Decision Logic: Rainfall & Moisture interplay
        irrigation_required = True
        priority = "MEDIUM"
        recommended_time = "Early Morning (06:00 AM - 08:30 AM)"
        next_suggested_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")

        if rainfall_forecast >= 15.0 or "rain" in current_weather.lower() or "storm" in current_weather.lower():
            irrigation_required = False
            priority = "LOW"
            water_amount = 0.0
            explanation = (
                f"Significant rainfall ({rainfall_forecast} mm) is forecasted over your area with '{current_weather}' conditions. "
                f"Irrigation should be SUSPENDED to prevent waterlogging, soil aeration loss, and fungal root pathogen buildup."
            )
            next_suggested_date = (datetime.now() + timedelta(days=4)).strftime("%Y-%m-%d")

        elif soil_moisture >= 65.0:
            irrigation_required = False
            priority = "LOW"
            water_amount = 0.0
            explanation = (
                f"Current soil moisture ({soil_moisture}%) is well above field capacity for {soil_type} soil. "
                f"Additional irrigation is not needed at this time."
            )
            next_suggested_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")

        elif soil_moisture < 35.0:
            irrigation_required = True
            priority = "HIGH"
            water_amount = round(daily_req * 1.5, 0)
            if temperature > 34:
                recommended_time = "Late Evening (05:30 PM - 07:30 PM) to minimize evaporative loss"
            explanation = (
                f"CRITICAL: Soil moisture has depleted to {soil_moisture}%, below the wilting threshold for {crop_name}. "
                f"Immediate irrigation is recommended during {growth_stage} stage to prevent stress-induced yield reduction."
            )
            next_suggested_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

        else:
            # 35% <= moisture < 65%
            irrigation_required = True
            priority = "MEDIUM"
            water_amount = round(daily_req, 0)
            explanation = (
                f"Moderate moisture ({soil_moisture}%). Planned irrigation of ~{int(water_amount):,} liters/acre "
                f"is recommended to sustain uniform vegetative growth."
            )
            next_suggested_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")

        # Weather note
        weather_condition_note = (
            f"Forecasted Rain: {rainfall_forecast} mm | Temp: {temperature}°C | Humidity: {humidity}%"
        )

        # Save advisory to DB
        advisory_record = IrrigationRecommendation(
            farmer_id=farmer_id,
            crop_name=crop_name,
            irrigation_required=irrigation_required,
            water_req_estimate_liters=water_amount,
            priority=priority,
            recommended_time=recommended_time,
            next_suggested_date=next_suggested_date,
            weather_condition_note=weather_condition_note,
            explanation=explanation
        )
        db.session.add(advisory_record)
        db.session.commit()

        return {
            "success": True,
            "crop_name": crop_name,
            "growth_stage": growth_stage,
            "soil_type": soil_type,
            "soil_moisture": soil_moisture,
            "irrigation_required": irrigation_required,
            "water_requirement_estimate_liters": water_amount,
            "priority": priority,
            "recommended_time": recommended_time,
            "next_suggested_date": next_suggested_date,
            "explanation": explanation,
            "weather_condition_note": weather_condition_note
        }
