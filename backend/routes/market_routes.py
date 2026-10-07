from flask import Blueprint, request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models.user import User
from services.market_service import MarketService

market_bp = Blueprint("market", __name__, url_prefix="/api/market")

@market_bp.route("/prices", methods=["GET"])
def get_market_prices():
    """Retrieve daily mandi commodity prices across markets."""
    crop = request.args.get("crop")
    district = request.args.get("district")
    limit = request.args.get("limit", default=50, type=int)

    prices = MarketService.get_latest_prices(crop_name=crop, district=district, limit=limit)
    return jsonify({
        "success": True,
        "count": len(prices),
        "prices": prices
    }), 200

@market_bp.route("/history", methods=["GET"])
def get_price_history():
    """Returns price trend timeline for charting in the frontend."""
    crop = request.args.get("crop", "Cotton")
    market_id = request.args.get("market_id", type=int)
    days = request.args.get("days", default=15, type=int)

    history_data = MarketService.get_crop_price_history(crop_name=crop, market_id=market_id, days=days)
    return jsonify({
        "success": True,
        "data": history_data
    }), 200

@market_bp.route("/nearby", methods=["GET"])
def get_nearby_markets():
    """Returns nearby agricultural markets with distances."""
    user_district = None
    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        if identity:
            u = User.query.get(int(identity))
            if u:
                user_district = u.district
    except Exception:
        pass

    district = request.args.get("district", user_district or "Kurnool")
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)

    markets = MarketService.get_nearby_markets(user_lat=lat, user_lon=lon, district=district)
    return jsonify({
        "success": True,
        "count": len(markets),
        "markets": markets
    }), 200
