import os
import requests
from datetime import datetime, timedelta
from flask import current_app
from database.db import db
from models.advisory import WeatherRecord
from models.notification import Notification

class WeatherService:
    @staticmethod
    def get_weather_data(location_query: str = "Guntur,IN", lat: float = None, lon: float = None, user_id: int = None):
        """
        Fetches live current weather and 5-day forecast from OpenWeatherMap API,
        or generates calibrated realistic weather data in DEMO_MODE.
        """
        api_key = os.getenv("WEATHER_API_KEY", "").strip()
        demo_mode = os.getenv("DEMO_MODE", "true").lower() in ("true", "1", "yes")

        # Attempt live API call if API key is provided
        if api_key and api_key != "your_openweathermap_api_key_here":
            try:
                base_url = "https://api.openweathermap.org/data/2.5"
                if lat is not None and lon is not None:
                    curr_url = f"{base_url}/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
                    fore_url = f"{base_url}/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
                else:
                    curr_url = f"{base_url}/weather?q={location_query}&appid={api_key}&units=metric"
                    fore_url = f"{base_url}/forecast?q={location_query}&appid={api_key}&units=metric"

                curr_resp = requests.get(curr_url, timeout=5)
                fore_resp = requests.get(fore_url, timeout=5)

                if curr_resp.status_code == 200:
                    curr_data = curr_resp.json()
                    fore_data = fore_resp.json() if fore_resp.status_code == 200 else {}
                    return WeatherService._format_live_response(curr_data, fore_data, location_query, user_id)
            except Exception as e:
                print(f"[WARN] Live Weather API connection failed: {e}. Falling back to demo data.")

        # Fallback to demo mode
        return WeatherService._generate_demo_weather(location_query, user_id)

    @staticmethod
    def _format_live_response(curr: dict, fore: dict, location_query: str, user_id: int = None):
        main = curr.get("main", {})
        wind = curr.get("wind", {})
        weather_list = curr.get("weather", [{}])
        cond = weather_list[0].get("main", "Clear")
        desc = weather_list[0].get("description", "clear sky").capitalize()

        temp = float(main.get("temp", 28.0))
        humidity = float(main.get("humidity", 65.0))
        wind_speed = float(wind.get("speed", 3.5)) * 3.6  # convert m/s to km/h
        rain_1h = float(curr.get("rain", {}).get("1h", 0.0))

        # Format 5-day forecast
        forecast_items = []
        if "list" in fore:
            # Pick one forecast reading per day (around 12:00 PM)
            seen_dates = set()
            for item in fore["list"]:
                dt_txt = item.get("dt_txt", "")
                date_part = dt_txt.split(" ")[0] if " " in dt_txt else ""
                if date_part not in seen_dates and len(forecast_items) < 5:
                    seen_dates.add(date_part)
                    f_main = item.get("main", {})
                    f_weather = item.get("weather", [{}])[0]
                    pop = item.get("pop", 0.0) * 100  # Probability of Precipitation
                    forecast_items.append({
                        "date": date_part,
                        "temp_min": round(f_main.get("temp_min", temp - 3), 1),
                        "temp_max": round(f_main.get("temp_max", temp + 3), 1),
                        "condition": f_weather.get("main", "Clear"),
                        "description": f_weather.get("description", "").capitalize(),
                        "rain_probability": round(pop, 0),
                        "icon": f_weather.get("icon", "01d")
                    })

        alerts = WeatherService.generate_farming_alerts(temp, humidity, rain_1h, wind_speed, user_id)

        return {
            "success": True,
            "source": "OpenWeatherMap Live API",
            "location": curr.get("name", location_query),
            "temperature": round(temp, 1),
            "feels_like": round(float(main.get("feels_like", temp)), 1),
            "humidity": round(humidity, 1),
            "wind_speed_kmh": round(wind_speed, 1),
            "rainfall_mm": round(rain_1h, 1),
            "condition": cond,
            "description": desc,
            "forecast_5_days": forecast_items,
            "farming_alerts": alerts
        }

    @staticmethod
    def _generate_demo_weather(location_query: str, user_id: int = None):
        """Generates realistic regional weather metrics for student demonstrations."""
        temp = 29.5
        humidity = 68.0
        wind_speed = 12.0
        rain_prob = 15.0

        today = datetime.now()
        forecast = [
            {"date": (today + timedelta(days=1)).strftime("%Y-%m-%d"), "temp_min": 22.0, "temp_max": 31.5, "condition": "Partly Cloudy", "description": "Scattered Clouds", "rain_probability": 20.0, "icon": "03d"},
            {"date": (today + timedelta(days=2)).strftime("%Y-%m-%d"), "temp_min": 23.0, "temp_max": 32.0, "condition": "Rain", "description": "Light Showers Expected", "rain_probability": 65.0, "icon": "10d"},
            {"date": (today + timedelta(days=3)).strftime("%Y-%m-%d"), "temp_min": 21.5, "temp_max": 28.0, "condition": "Rain", "description": "Moderate Rain", "rain_probability": 80.0, "icon": "10d"},
            {"date": (today + timedelta(days=4)).strftime("%Y-%m-%d"), "temp_min": 20.0, "temp_max": 30.0, "condition": "Clear", "description": "Sunny & Clear", "rain_probability": 10.0, "icon": "01d"},
            {"date": (today + timedelta(days=5)).strftime("%Y-%m-%d"), "temp_min": 21.0, "temp_max": 31.0, "condition": "Clear", "description": "Clear Sky", "rain_probability": 5.0, "icon": "01d"},
        ]

        alerts = WeatherService.generate_farming_alerts(temp, humidity, 0.0, wind_speed, user_id)

        return {
            "success": True,
            "source": "Agronomic Demo Mode Simulator (OpenWeatherMap compatible)",
            "location": location_query or "Kurnool, Andhra Pradesh",
            "temperature": temp,
            "feels_like": 31.2,
            "humidity": humidity,
            "wind_speed_kmh": wind_speed,
            "rainfall_mm": 0.0,
            "condition": "Partly Cloudy",
            "description": "Scattered clouds with mild breeze",
            "forecast_5_days": forecast,
            "farming_alerts": alerts
        }

    @staticmethod
    def generate_farming_alerts(temp: float, humidity: float, rainfall: float, wind_speed: float, user_id: int = None) -> list:
        """
        Evaluates microclimate thresholds to generate actionable agricultural alerts
        with LOW, MEDIUM, HIGH priority ratings.
        """
        alerts = []

        # 1. Rain / Irrigation Alert
        if rainfall > 20.0:
            alerts.append({
                "id": "heavy_rain",
                "title": "Heavy Rain Alert",
                "message": f"Heavy rainfall ({rainfall} mm) recorded. Avoid field irrigation and ensure drain outlets are clear.",
                "priority": "HIGH",
                "category": "WEATHER"
            })
        elif rainfall > 5.0:
            alerts.append({
                "id": "moderate_rain",
                "title": "Moderate Rain Advisory",
                "message": "Light-to-moderate rain observed. Postpone planned chemical applications and top-dressing.",
                "priority": "MEDIUM",
                "category": "WEATHER"
            })

        # 2. Heat Stress Alert
        if temp > 36.0:
            alerts.append({
                "id": "heat_stress",
                "title": "High Temperature Warning",
                "message": f"Excessive ambient heat ({temp}°C). High evapotranspiration rate. Irrigate during cooler early morning or late evening hours.",
                "priority": "HIGH",
                "category": "WEATHER"
            })

        # 3. Disease-Favourable Conditions
        if humidity > 80.0 and 22.0 <= temp <= 30.0:
            alerts.append({
                "id": "disease_favourable",
                "title": "Disease-Favourable Microclimate",
                "message": f"High relative humidity ({humidity}%) at {temp}°C creates prime conditions for fungal leaf blast and late blight spore multiplication. Inspect crops closely.",
                "priority": "HIGH",
                "category": "DISEASE"
            })

        # 4. Wind Speed / Spraying Suitability
        if wind_speed > 25.0:
            alerts.append({
                "id": "strong_winds",
                "title": "Strong Wind Advisory",
                "message": f"Wind gusts at {wind_speed} km/h will cause severe droplet drift. DO NOT spray pesticides or foliar fertilizers.",
                "priority": "MEDIUM",
                "category": "WEATHER"
            })
        elif wind_speed <= 15.0 and rainfall == 0.0 and humidity < 75.0:
            alerts.append({
                "id": "optimal_spray",
                "title": "Ideal Spraying Condition",
                "message": "Gentle winds (<15 km/h) and dry conditions. Excellent window for pesticide, micronutrient, and herbicide sprays.",
                "priority": "LOW",
                "category": "WEATHER"
            })

        # Persist alert notifications for authenticated user
        if user_id:
            try:
                for alert in alerts:
                    # Avoid duplicate recent notifications
                    existing = Notification.query.filter_by(
                        user_id=user_id,
                        title=alert["title"],
                        is_read=False
                    ).first()
                    if not existing:
                        db.session.add(Notification(
                            user_id=user_id,
                            title=alert["title"],
                            message=alert["message"],
                            category=alert["category"],
                            priority=alert["priority"]
                        ))
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"[WARN] Error saving notification: {e}")

        return alerts
