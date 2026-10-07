from flask import Blueprint, request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models.chat import ChatMessage
from services.chatbot_service import ChatbotService

chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/api/chatbot")

@chatbot_bp.route("/message", methods=["POST"])
@chatbot_bp.route("/query", methods=["POST"])
def send_message():
    """Handles farmer chatbot inquiries and returns actionable agronomic advice."""
    user_id = None
    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        if identity:
            user_id = int(identity)
    except Exception:
        pass

    data = request.get_json() or {}
    message = data.get("message", "").strip()
    session_id = data.get("session_id")
    language = data.get("language", "en")
    preferred_provider = data.get("provider")

    if not message:
        return jsonify({"success": False, "message": "Message text cannot be empty."}), 400

    response = ChatbotService.process_message(
        user_message=message,
        session_id=session_id,
        user_id=user_id,
        language=language,
        preferred_provider=preferred_provider
    )

    return jsonify({
        "success": True,
        **response
    }), 200

@chatbot_bp.route("/models", methods=["GET"])
def get_llm_models():
    """Returns all available LLM models and status."""
    from services.llm_service import LLMService
    return jsonify({
        "success": True,
        "providers": LLMService.get_available_providers()
    }), 200

@chatbot_bp.route("/ask-llm", methods=["POST"])
def direct_llm_query():
    """Direct agronomic query to LLM engine."""
    from services.llm_service import LLMService
    data = request.get_json() or {}
    prompt = data.get("prompt", "").strip()
    provider = data.get("provider")
    context = data.get("context", {})

    if not prompt:
        return jsonify({"success": False, "message": "Prompt is required."}), 400

    result = LLMService.generate_response(prompt=prompt, context=context, preferred_provider=provider)
    return jsonify({
        "success": True,
        **result
    }), 200

@chatbot_bp.route("/history", methods=["GET"])
def get_chat_history():
    """Retrieves session interaction history."""
    session_id = request.args.get("session_id")
    user_id = None

    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        if identity:
            user_id = int(identity)
    except Exception:
        pass

    query = ChatMessage.query
    if session_id:
        query = query.filter_by(session_id=session_id)
    elif user_id:
        query = query.filter_by(user_id=user_id)
    else:
        return jsonify({"success": True, "messages": []}), 200

    messages = query.order_by(ChatMessage.created_at.asc()).limit(50).all()
    return jsonify({
        "success": True,
        "count": len(messages),
        "messages": [m.to_dict() for m in messages]
    }), 200
