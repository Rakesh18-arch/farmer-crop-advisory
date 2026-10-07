from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    preferred_language = db.Column(db.String(10), default="en")  # 'en', 'te', 'hi'
    state = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    village = db.Column(db.String(100), nullable=True)
    role = db.Column(db.String(20), default="farmer")  # 'farmer' or 'admin'
    is_active = db.Column(db.Boolean, default=True)
    
    # Password Reset Workflow fields
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    farmer_profile = db.relationship("FarmerProfile", backref="user", uselist=False, cascade="all, delete-orphan")
    notifications = db.relationship("Notification", backref="user", lazy=True, cascade="all, delete-orphan")
    chat_messages = db.relationship("ChatMessage", backref="user", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password: str):
        """Hash and save user password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify entered password against stored hash."""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Serialize user object without sensitive fields."""
        return {
            "id": self.id,
            "full_name": self.full_name,
            "phone_number": self.phone_number,
            "email": self.email,
            "preferred_language": self.preferred_language,
            "state": self.state,
            "district": self.district,
            "village": self.village,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "has_profile": self.farmer_profile is not None
        }
