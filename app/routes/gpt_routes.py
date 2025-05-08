from flask import Blueprint, request, jsonify
from openai import OpenAI
import httpx, os, traceback
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.message import Message
from app.models.user import User
from app.extensions import db




bp = Blueprint("gpt", __name__, url_prefix="/gpt")

http_client = httpx.Client(
    timeout=30.0,
    limits=httpx.Limits(max_connections=100),
    follow_redirects=True
)

client = OpenAI(
    api_key=os.getenv("API_KEY"),
    http_client=http_client
)


@bp.route("/ask", methods=["POST"])
@jwt_required()
def ask_gpt():
    try:
        user_id = get_jwt_identity()
        message = request.get_json().get("message")

        if not message:
            return jsonify({"status": "error", "message": "Сообщение отсутствует"}), 400

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}],
            temperature=0.7,
            max_tokens=1000
        )
        reply = response.choices[0].message.content

        new_message = Message(prompt=message, response=reply, user_id=user_id)
        db.session.add(new_message)
        db.session.commit()

        return jsonify({
            "status": "success",
            "response": reply
        }), 200

    except Exception as e:
        print("❌ GPT ERROR:", e)
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500


@bp.route("/history", methods=["GET"])
@jwt_required()
def get_history():
    user_id = get_jwt_identity()
    messages = Message.query.filter_by(user_id=user_id).all()
    return jsonify([msg.to_dict() for msg in messages]), 200
