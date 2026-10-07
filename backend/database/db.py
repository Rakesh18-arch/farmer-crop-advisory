from flask_sqlalchemy import SQLAlchemy

# Initialize global SQLAlchemy instance
db = SQLAlchemy()

def init_db(app):
    """Binds SQLAlchemy to the Flask app and ensures tables exist."""
    db.init_app(app)
    with app.app_context():
        # Ensure all models are imported before creating tables
        from models import (
            user, farm, crop, disease, market, advisory, notification, chat
        )
        db.create_all()
