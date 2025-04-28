from app.models.user import User
from app.extensions import db



def get_all_users():
    return User.query.all()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_users_by_name_start(letter):
    return User.query.filter(User.username.startswith(letter)).all()



def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"message": "Пользователь не найден"}, 404
    db.session.delete(user)
    db.session.commit()
    return {"message": "Пользователь удалён"}, 200
