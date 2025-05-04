from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
from app.models.user import User
from app.extensions import db
from app.schemas.user_schema import RegisterSchema, LoginSchema
from app.utils.response import success_response, error_response
from app.services.token_blacklist import blacklist



bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    errors = RegisterSchema().validate(data)
    if errors:
        return error_response(str(errors))

    if User.query.filter_by(username=data["username"]).first():
        return error_response("Пользователь уже существует", 409)

    hashed_password = generate_password_hash(data["password"])
    new_user = User(username=data["username"], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return success_response(message="Регистрация успешна", status=201)



@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    errors = LoginSchema().validate(data)
    if errors:
        return error_response(str(errors))

    user = User.query.filter_by(username=data["username"]).first()
    if not user or not check_password_hash(user.password, data["password"]):
        return error_response("Неверный логин или пароль", 401)

    token = create_access_token(identity=str(user.id))
    return success_response({"token": token})


@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    blacklist.add(jti)
    return success_response(message="Вы вышли из системы")


@bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    return success_response({"username": user.username})
