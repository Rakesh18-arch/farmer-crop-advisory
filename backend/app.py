import os
import sys

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config_by_name
from database.db import db, init_db

def create_app(config_name=None):
    """Application factory for Farmer Crop Advisory Platform."""
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name["default"]))

    # Setup Cross-Origin Resource Sharing
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # Setup JWT Manager
    jwt = JWTManager(app)

    @jwt.unauthorized_loader
    def unauthorized_response(callback):
        return jsonify({
            "success": False,
            "message": "Missing Authorization header or token."
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_response(callback):
        return jsonify({
            "success": False,
            "message": "Signature verification failed or token is malformed."
        }), 401

    @jwt.expired_token_loader
    def expired_token_response(jwt_header, jwt_payload):
        return jsonify({
            "success": False,
            "message": "Token has expired. Please log in again."
        }), 401

    # Ensure Uploads directory exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Initialize Database
    init_db(app)

    # Register Blueprints
    from routes.auth_routes import auth_bp
    from routes.farmer_routes import farmer_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(farmer_bp)

    # Register modular blueprints safely as they become available
    modular_blueprints = [
        ("routes.crop_routes", "crop_bp"),
        ("routes.fertilizer_routes", "fertilizer_bp"),
        ("routes.irrigation_routes", "irrigation_bp"),
        ("routes.disease_routes", "disease_bp"),
        ("routes.weather_routes", "weather_bp"),
        ("routes.market_routes", "market_bp"),
        ("routes.schemes_routes", "schemes_bp"),
        ("routes.chatbot_routes", "chatbot_bp"),
        ("routes.notification_routes", "notification_bp"),
        ("routes.admin_routes", "admin_bp")
    ]

    for mod_name, bp_name in modular_blueprints:
        try:
            import importlib
            module = importlib.import_module(mod_name)
            bp = getattr(module, bp_name)
            app.register_blueprint(bp)
        except (ImportError, AttributeError):
            pass

    # Support /api/chat alias for frontend compatibility
    try:
        from routes.chatbot_routes import chatbot_bp
        app.register_blueprint(chatbot_bp, name="chat_alias", url_prefix="/api/chat")
    except Exception as e:
        print(f"[WARN] Error registering chat alias: {e}")

    # Global Health Check & System Status
    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "healthy",
            "service": "Farmer Crop Advisory Platform API",
            "environment": config_name,
            "demo_mode": app.config.get("DEMO_MODE", True),
            "version": "1.0.0"
        }), 200

    # Serve Built React Frontend SPA from frontend/dist
    base_path = os.path.dirname(__file__)
    possible_dist_dirs = [
        os.path.abspath(os.path.join(base_path, "..", "frontend", "dist")),
        os.path.abspath(os.path.join(base_path, "frontend", "dist")),
        os.path.abspath(os.path.join(base_path, "dist")),
        os.path.abspath("/app/frontend/dist")
    ]
    dist_dir = next((d for d in possible_dist_dirs if os.path.exists(d)), possible_dist_dirs[0])

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_frontend(path):
        if path.startswith("api/"):
            return jsonify({
                "success": False,
                "message": "The requested API endpoint was not found on this server."
            }), 404

        target_file = os.path.join(dist_dir, path)
        if path != "" and os.path.exists(target_file) and os.path.isfile(target_file):
            return send_from_directory(dist_dir, path)
        elif os.path.exists(os.path.join(dist_dir, "index.html")):
            return send_from_directory(dist_dir, "index.html")
        else:
            return jsonify({
                "status": "healthy",
                "service": "Farmer Crop Advisory Platform API",
                "message": "Frontend build not found in frontend/dist. Run 'npm run build' in frontend/ to serve React UI."
            })

    @app.errorhandler(500)
    def internal_error_handler(e):
        return jsonify({
            "success": False,
            "message": "An internal server error occurred. Please try again later."
        }), 500

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 5000))
    print(f"[START] Farmer Crop Advisory API running at http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
