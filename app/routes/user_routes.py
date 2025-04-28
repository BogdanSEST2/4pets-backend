from flask import Blueprint, jsonify, request
from app.services import user_service




bp = Blueprint('user', __name__)


@bp.route('/users', methods=['GET'])
def get_users():
    users = user_service.get_all_users()
    users_list = [{"id": user.id, "username": user.username} for user in users]
    return jsonify(users_list), 200


@bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_service.get_user_by_id(user_id)
    if user:
        return jsonify({"id": user.id, "username": user.username}), 200
    return jsonify({"message": "Пользователь не найден"}), 404


@bp.route('/users/by_letter/<letter>', methods=['GET'])
def get_users_by_letter(letter):
    users = user_service.get_users_by_name_start(letter)
    users_list = [{"id": user.id, "username": user.username} for user in users]
    return jsonify(users_list), 200


@bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    success = user_service.delete_user(user_id)
    if success:
        return jsonify({"message": "Пользователь удалён"}), 200
    return jsonify({"message": "Пользователь не найден"}), 404
