from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.db import db
from models.notification import Notification

notification_bp = Blueprint("notification", __name__, url_prefix="/api/notifications")

@notification_bp.route("", methods=["GET"])
@jwt_required()
def get_user_notifications():
    """Retrieve in-app notifications for authenticated farmer."""
    user_id = int(get_jwt_identity())
    notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).limit(30).all()
    unread_count = Notification.query.filter_by(user_id=user_id, is_read=False).count()
    return jsonify({
        "success": True,
        "unread_count": unread_count,
        "count": len(notifications),
        "notifications": [n.to_dict() for n in notifications]
    }), 200

@notification_bp.route("/<int:notification_id>/read", methods=["PUT"])
@jwt_required()
def mark_notification_read(notification_id):
    """Mark a single notification as read."""
    user_id = int(get_jwt_identity())
    notif = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
    if not notif:
        return jsonify({"success": False, "message": "Notification not found."}), 404

    notif.is_read = True
    db.session.commit()
    return jsonify({"success": True, "message": "Notification marked as read."}), 200

@notification_bp.route("/mark-all-read", methods=["PUT"])
@jwt_required()
def mark_all_read():
    """Mark all unread notifications as read."""
    user_id = int(get_jwt_identity())
    Notification.query.filter_by(user_id=user_id, is_read=False).update({"is_read": True})
    db.session.commit()
    return jsonify({"success": True, "message": "All notifications marked as read."}), 200
