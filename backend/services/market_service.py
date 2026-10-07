import math
from datetime import date, datetime, timedelta
from database.db import db
from models.market import Market, MarketPrice

class MarketService:
    @staticmethod
    def get_latest_prices(crop_name: str = None, district: str = None, limit: int = 50) -> list:
        """
        Retrieves real-time/recent mandi commodity rates.
        Supports filtering by crop and district.
        """
        query = db.session.query(MarketPrice).join(Market)
        if crop_name:
            query = query.filter(MarketPrice.crop_name.ilike(f"%{crop_name}%"))
        if district:
            query = query.filter(Market.district.ilike(f"%{district}%"))

        records = query.order_by(MarketPrice.price_date.desc(), MarketPrice.modal_price.desc()).limit(limit).all()
        return [r.to_dict() for r in records]

    @staticmethod
    def get_crop_price_history(crop_name: str, market_id: int = None, days: int = 15) -> dict:
        """
        Generates daily price trend history for charting in the frontend.
        """
        today = date.today()
        start_date = today - timedelta(days=days)

        query = MarketPrice.query.filter(
            MarketPrice.crop_name.ilike(f"%{crop_name}%"),
            MarketPrice.price_date >= start_date
        )
        if market_id:
            query = query.filter_by(market_id=market_id)

        history_records = query.order_by(MarketPrice.price_date.asc()).all()

        history_points = []
        if history_records:
            for r in history_records:
                history_points.append({
                    "date": r.price_date.isoformat(),
                    "min_price": r.min_price,
                    "max_price": r.max_price,
                    "modal_price": r.modal_price
                })
        else:
            # Fallback simulated trend if historical DB points are sparse
            base_prices = {
                "Cotton": 7200, "Rice": 3200, "Maize": 2250, 
                "Chilli": 17800, "Tomato": 1650, "Groundnut": 6300,
                "Wheat": 2450, "Soybean": 4800
            }
            base = base_prices.get(crop_name.capitalize(), 3000)
            for i in range(days, -1, -1):
                d = today - timedelta(days=i)
                fluctuation = int(math.sin(i) * (base * 0.04))
                modal = base + fluctuation
                history_points.append({
                    "date": d.isoformat(),
                    "min_price": modal - int(base * 0.05),
                    "max_price": modal + int(base * 0.05),
                    "modal_price": modal
                })

        # Calculate general price trend
        if len(history_points) >= 2:
            first_p = history_points[0]["modal_price"]
            last_p = history_points[-1]["modal_price"]
            diff = last_p - first_p
            pct_change = round((diff / first_p) * 100, 2)
            trend_str = "UP" if diff > 0 else ("DOWN" if diff < 0 else "STABLE")
        else:
            pct_change = 0.0
            trend_str = "STABLE"

        return {
            "crop_name": crop_name,
            "period_days": days,
            "trend": trend_str,
            "change_percent": pct_change,
            "history": history_points
        }

    @staticmethod
    def get_nearby_markets(user_lat: float = None, user_lon: float = None, 
                           district: str = None, radius_km: float = 100.0) -> list:
        """
        Finds markets proximate to the farmer's district or GPS coordinates
        using the Haversine distance formula.
        """
        markets = Market.query.filter_by(is_active=True).all()
        results = []

        # Reference district coordinates for demo
        district_coords = {
            "Kurnool": (15.8281, 78.0373),
            "Guntur": (16.3067, 80.4365),
            "Warangal": (17.9689, 79.5941),
            "Pune": (18.5204, 73.8567),
            "Ludhiana": (30.9010, 75.8573)
        }

        origin_lat = user_lat
        origin_lon = user_lon

        if (origin_lat is None or origin_lon is None) and district:
            normalized_district = district.strip().capitalize()
            if normalized_district in district_coords:
                origin_lat, origin_lon = district_coords[normalized_district]

        for m in markets:
            dist = None
            if origin_lat is not None and origin_lon is not None and m.latitude and m.longitude:
                # Haversine distance
                lat1, lon1 = math.radians(origin_lat), math.radians(origin_lon)
                lat2, lon2 = math.radians(m.latitude), math.radians(m.longitude)
                dlat = lat2 - lat1
                dlon = lon2 - lon1
                a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                dist = round(6371.0 * c, 1)  # Earth radius in KM

            # Fetch currently traded commodities in this market
            traded_crops = [p.crop_name for p in m.prices]
            traded_summary = list(set(traded_crops)) if traded_crops else ["Food Grains", "Commercial Crops"]

            market_data = m.to_dict()
            market_data["distance_km"] = dist
            market_data["main_crops_traded"] = traded_summary
            market_data["commodities_count"] = len(m.prices)
            results.append(market_data)

        # Sort by distance if calculated, otherwise by district match
        if origin_lat is not None:
            results.sort(key=lambda x: (x["distance_km"] is None, x["distance_km"] or 9999))
        elif district:
            results.sort(key=lambda x: x["district"].lower() != district.lower())

        return results
