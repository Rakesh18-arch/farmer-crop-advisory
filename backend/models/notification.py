from datetime import datetime
from database.db import db

class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default="WEATHER")  # WEATHER, IRRIGATION, DISEASE, MARKET, SCHEME, SYSTEM
    priority = db.Column(db.String(20), default="LOW")      # LOW, MEDIUM, HIGH
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "message": self.message,
            "category": self.category,
            "priority": self.priority,
            "is_read": self.is_read,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
