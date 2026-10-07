from flask import Blueprint, request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models.user import User
from services.weather_service import WeatherService

weather_bp = Blueprint("weather", __name__, url_prefix="/api/weather")

@weather_bp.route("/current", methods=["GET"])
def get_current_weather():
    """Retrieve current weather, forecast, and farming alerts for farmer's location."""
    user_id = None
    default_location = "Kurnool, Andhra Pradesh"

    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        if identity:
            user_id = int(identity)
            user = User.query.get(user_id)
            if user and user.district:
                default_location = f"{user.district}, {user.state}"
    except Exception:
        pass

    location = request.args.get("location", default_location)
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)

    data = WeatherService.get_weather_data(
        location_query=location,
        lat=lat,
        lon=lon,
        user_id=user_id
    )

    return jsonify(data), 200

@weather_bp.route("/forecast", methods=["GET"])
def get_forecast():
    """Retrieve 5-day weather forecast with rain probability."""
    location = request.args.get("location", "Kurnool, Andhra Pradesh")
    data = WeatherService.get_weather_data(location_query=location)
    return jsonify({
        "success": True,
        "location": data.get("location"),
        "forecast": data.get("forecast_5_days", [])
    }), 200

@weather_bp.route("/alerts", methods=["GET"])
def get_weather_alerts():
    """Retrieve weather-driven farming warnings with priority levels."""
    location = request.args.get("location", "Kurnool, Andhra Pradesh")
    data = WeatherService.get_weather_data(location_query=location)
    return jsonify({
        "success": True,
        "location": data.get("location"),
        "alerts": data.get("farming_alerts", [])
    }), 200
