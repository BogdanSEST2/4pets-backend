from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.models.user import User
from app.extensions import db
from app.schemas.user_schema import RegisterSchema, LoginSchema
from app.utils.response import success_response, error_response



def register_user(data):
    errors = RegisterSchema().validate(data)
    if errors:
        return error_response(str(errors))

    if User.query.filter_by(username=data["username"]).first():
        return error_response("Пользователь уже существует", 400)

    hashed_password = generate_password_hash(data["password"])
    new_user = User(username=data["username"], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    token = create_access_token(identity=str(new_user.id))

    return success_response({"token": token}, message="Регистрация успешна", status=201)


def login_user(data):
    errors = LoginSchema().validate(data)
    if errors:
        return error_response(str(errors))

    user = User.query.filter_by(username=data["username"]).first()
    if not user or not check_password_hash(user.password, data["password"]):
        return error_response("Неверный логин или пароль", 401)

    token = create_access_token(identity=str(user.id))
    return success_response({"token": token})


def logout_user(jti):
    from app.services.token_blacklist import blacklist
    blacklist.add(jti)
    return success_response(message="Вы вышли из системы")


def get_user_info(user_id):
    user = User.query.get(user_id)
    if not user:
        return error_response("Пользователь не найден", 404)
    return success_response({"username": user.username})
