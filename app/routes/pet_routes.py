from flask import Blueprint, jsonify, request
from app.services import pet_service



bp = Blueprint('pet', __name__)


@bp.route('/pets', methods=['GET'])
def get_pets():
    pets = pet_service.get_pets()
    return jsonify(pets), 200


@bp.route('/pets', methods=['POST'])
def add_pet():
    data = request.get_json()
    owner_id = data.get('owner_id')
    pet_data = data.get('pet')
    result = pet_service.add_pet(owner_id, pet_data)
    return jsonify(result), 201

