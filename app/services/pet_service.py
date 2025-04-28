def get_pets():
    return {"pets": []}


def add_pet(owner_id, pet_data):
    return {
        "message": f"Питомец добавлен для владельца {owner_id}",
        "data": pet_data
    }
