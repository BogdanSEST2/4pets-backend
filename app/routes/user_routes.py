from flask import Blueprint, jsonify
from app.models.user import User
from app.extensions import db

bp = Blueprint('user', __name__)

@bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{"id": user.id, "username": user.username} for user in users]
    return jsonify(users_list), 200
