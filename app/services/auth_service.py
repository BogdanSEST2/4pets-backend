from app.models.user import User
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token



def register_user(username, password):
    if User.query.filter_by(username=username).first():
        return {"message": "Пользователь уже существует"}, 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return {"message": "Регистрация успешна"}, 201


def login_user(username, password):
    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return {"message": "Неверный логин или пароль"}, 401

    access_token = create_access_token(identity=user.id)
    return {"access_token": access_token}, 200
