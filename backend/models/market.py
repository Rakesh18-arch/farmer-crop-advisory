from datetime import datetime, date
from database.db import db

class Market(db.Model):
    __tablename__ = "markets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    district = db.Column(db.String(100), nullable=False, index=True)
    state = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    contact_number = db.Column(db.String(50), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    prices = db.relationship("MarketPrice", backref="market", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "district": self.district,
            "state": self.state,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "contact_number": self.contact_number,
            "is_active": self.is_active
        }

class MarketPrice(db.Model):
    __tablename__ = "market_prices"

    id = db.Column(db.Integer, primary_key=True)
    market_id = db.Column(db.Integer, db.ForeignKey("markets.id"), nullable=False)
    crop_name = db.Column(db.String(100), nullable=False, index=True)
    variety = db.Column(db.String(100), default="Common")
    min_price = db.Column(db.Float, nullable=False)    # Rs / Quintal
    max_price = db.Column(db.Float, nullable=False)    # Rs / Quintal
    modal_price = db.Column(db.Float, nullable=False)  # Rs / Quintal
    price_date = db.Column(db.Date, default=date.today)
    price_trend = db.Column(db.String(20), default="STABLE")  # UP, DOWN, STABLE
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "market_id": self.market_id,
            "market_name": self.market.name if self.market else None,
            "district": self.market.district if self.market else None,
            "crop_name": self.crop_name,
            "variety": self.variety,
            "min_price": self.min_price,
            "max_price": self.max_price,
            "modal_price": self.modal_price,
            "price_date": self.price_date.isoformat() if self.price_date else None,
            "price_trend": self.price_trend
        }
