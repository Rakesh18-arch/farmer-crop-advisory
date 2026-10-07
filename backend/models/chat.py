from datetime import datetime
from database.db import db

class ChatMessage(db.Model):
    __tablename__ = "chat_messages"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    session_id = db.Column(db.String(100), nullable=False, index=True)
    sender = db.Column(db.String(20), nullable=False)  # 'user' or 'bot'
    message_text = db.Column(db.Text, nullable=False)
    detected_intent = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "sender": self.sender,
            "message_text": self.message_text,
            "detected_intent": self.detected_intent,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
