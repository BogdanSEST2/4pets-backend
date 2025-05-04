from app.models.pet import Pet
from app.extensions import db



def get_pets():
    pets = Pet.query.all()
    return {
        "pets": [
            {"id": pet.id, "name": pet.name, "type": pet.type, "age": pet.age, "owner_id": pet.owner_id}
            for pet in pets
        ]
    }


def add_pet(owner_id, pet_data):
    from app.models.pet import Pet
    from app.extensions import db

    pet = Pet(name=pet_data["name"], type=pet_data["type"], age=pet_data["age"], owner_id=owner_id)
    db.session.add(pet)
    db.session.commit()

    return {
        "message": f"Питомец добавлен для владельца {owner_id}",
        "pet": {
            "id": pet.id,
            "name": pet.name,
            "type": pet.type,
            "age": pet.age,
            "owner_id": pet.owner_id
        }
    }



def get_pets_by_owner(owner_id):
    pets = Pet.query.filter_by(owner_id=owner_id).all()
    return {
        "pets": [
            {
                "id": pet.id,
                "name": pet.name,
                "type": pet.type,
                "age": pet.age,
                "owner_id": pet.owner_id
            }
            for pet in pets
        ]
    }


def delete_pet(pet_id):
    pet = db.session.get(Pet, pet_id)
    if not pet:
        return {"message": f"Питомец с id={pet_id} не найден"}, 404

    db.session.delete(pet)
    db.session.commit()
    return {"message": f"Питомец с id={pet_id} успешно удалён"}



def delete_pets_by_owner(owner_id):
    pets = Pet.query.filter_by(owner_id=owner_id).all()
    if not pets:
        return {"message": f"У пользователя с id={owner_id} нет питомцев"}

    for pet in pets:
        db.session.delete(pet)

    db.session.commit()
    return {"message": f"Удалены все питомцы пользователя с id={owner_id}"}
