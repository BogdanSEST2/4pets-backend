from flask import Blueprint, jsonify, request
from app.services import pet_service
from app.models.pet import Pet
from app.extensions import db



bp = Blueprint('pet_bp', __name__)


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


@bp.route('/owner/<int:owner_id>', methods=['GET'])
def get_pets_for_owner(owner_id):
    result = pet_service.get_pets_by_owner(owner_id)
    return jsonify(result), 200


@bp.route('/pets/<int:pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    result = pet_service.delete_pet(pet_id)
    return jsonify(result), 200


@bp.route('/owner/<int:owner_id>', methods=['DELETE'])
def delete_pets_by_owner(owner_id):
    db.session.query(Pet).filter_by(owner_id=owner_id).delete()
    db.session.commit()
    return jsonify({"message": f"Все питомцы пользователя с id {owner_id} удалены"}), 200


@bp.route('/pets/<int:pet_id>', methods=['PUT'])
def update_pet(pet_id):
    data = request.get_json()
    pet = db.session.query(Pet).filter_by(id=pet_id).first()
    if not pet:
        return jsonify({"message": "Питомец не найден"}), 404

    pet.name = data.get("name", pet.name)
    pet.type = data.get("type", pet.type)
    pet.age = data.get("age", pet.age)
    db.session.commit()

    return jsonify({"message": f"Питомец с id {pet_id} обновлён"}), 200
