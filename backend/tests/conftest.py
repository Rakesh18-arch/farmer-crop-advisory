import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from database.db import db
from models.user import User
from models.farm import FarmerProfile

@pytest.fixture
def app():
    test_app = create_app("testing")
    with test_app.app_context():
        db.create_all()
        from models.market import Market, MarketPrice
        from models.advisory import GovernmentScheme
        m = Market(name="Kurnool APMC", district="Kurnool", state="Andhra Pradesh", latitude=15.82, longitude=78.03)
        db.session.add(m)
        db.session.flush()
        mp = MarketPrice(market_id=m.id, crop_name="Cotton", min_price=7000, max_price=7500, modal_price=7250)
        s = GovernmentScheme(
            scheme_name="PM-KISAN", description="Income support", eligibility="Land-owning farmers",
            benefits="Rs 6,000/yr", required_documents="Aadhaar", applicable_state="All India"
        )
        db.session.add_all([mp, s])
        db.session.commit()

        yield test_app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    # Register test farmer
    register_payload = {
        "full_name": "Test Farmer",
        "phone_number": "9998887770",
        "email": "testfarmer@advisory.org",
        "password": "Password@123",
        "state": "Andhra Pradesh",
        "district": "Guntur",
        "village": "Tenali",
        "preferred_language": "en"
    }
    res = client.post("/api/auth/register", json=register_payload)
    token = res.get_json()["access_token"]
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

@pytest.fixture
def admin_headers(app, client):
    with app.app_context():
        admin = User(
            full_name="Admin Officer",
            phone_number="9990001112",
            email="admin@advisory.org",
            role="admin",
            state="National",
            district="Central"
        )
        admin.set_password("Admin@123")
        db.session.add(admin)
        db.session.commit()

    res = client.post("/api/auth/login", json={"email": "admin@advisory.org", "password": "Admin@123"})
    token = res.get_json()["access_token"]
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

