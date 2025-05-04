from flask import Blueprint, jsonify, request
from app.services import chat_service



bp = Blueprint('chat', __name__) 

@bp.route('/chats', methods=['GET'])
def get_chats():
    chats = chat_service.get_all_chats()
    return jsonify(chats), 200

@bp.route('/chats/<int:chat_id>/message', methods=['POST'])
def send_message(chat_id):
    data = request.get_json()
    user_id = data.get('user_id')
    message = data.get('message')
    result = chat_service.send_message(chat_id, user_id, message)
    return jsonify(result), 201
