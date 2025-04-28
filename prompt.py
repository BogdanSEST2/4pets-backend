'''

Блять, короче. Вот структура моего проекта на Python Flask. Я хочу, чтобы ты помог мне разобраться, всё ли у меня правильно реализовано.

Вот структура проекта:

app/
    config/
        __init__.py
        config.py
        default.py
        development.py
        production.py
    models/
        __init__.py
        chat.py
        pet.py
        post.py
        user.py
    routes/
        __init__.py
        auth_routes.py
        chat_routes.py
        pet_routes.py
        post_routes.py
        user_routes.py
    services/
        __init__.py
        auth_service.py
        chat_service.py
        pet_service.py
        user_service.py
    utils/
        __init__.py
        constants.py
        helpers.py
        validators.py
        extensions.py
    main.py
instance/
migrations/
tests/
.env
requirements.txt
run.py
README.md



Теперь я тебе дам весь код каждого файла по очереди. После этого:
Скажи мне, всё ли сделано правильно?
Если где-то херня — скажи, в каком именно файле и в какой папке что надо переписать или добавить, чтобы всё заработало.
После твоих предложений я хочу, чтобы весь проект запускался нормально.
Как мне всё это протестировать? Какие тесты написать? Может быть, тесты есть у меня в папке tests, и ты скажешь, как их запустить.
Подскажи, что ещё можно улучшить.
Цель: чтобы я вообще не парился, всё заработало, и я мог спокойно тестировать и дорабатывать свой проект.



app/config/__init__.py:

# пусто






app/config/config.py:

import os



class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key')

    


    




app/config/default.py:

from .config import Config



class DefaultConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///default_db.sqlite3'

    


    





app/config/development.py:

# пусто





app/config/production.py:


import os
from .config import Config



class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///prod_db.sqlite3')




    





















app/models/__init__.py:

from .user import User
from .pet import Pet
from .chat import Chat
from .post import Post



__all__ = ['User', 'Pet', 'Chat', 'Post']






app/models/chat.py:

from app.extensions import db



class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Chat {self.title}>"

        





app/models/pet.py:


from app.extensions import db



class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50))
    age = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Pet {self.name}>"

        




app/models/post.py:


from app.extensions import db



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Post {self.id}>"

        






app/models/user.py:

from app.extensions import db



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

        














app/routes/__init__.py:

from .auth_routes import bp as auth_bp
from .user_routes import bp as user_bp
from .pet_routes import bp as pet_bp
from .chat_routes import bp as chat_bp
from .post_routes import bp as post_bp


__all__ = ['auth_bp', 'user_bp', 'pet_bp', 'chat_bp', 'post_bp']







app/routes/auth_routes.py:

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app.extensions import db



bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Пользователь уже существует"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Регистрация успешна"}), 201


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Неверный логин или пароль"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200


@bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({"username": user.username}), 200

    








app/routes/chat_routes.py:

from flask import Blueprint, jsonify, request
from app.services import user_service



bp = Blueprint('user', __name__)


@bp.route('/users', methods=['GET'])
def get_users():
    users = user_service.get_all_users()
    return jsonify(users), 200


@bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    result = user_service.get_user_by_id(user_id)
    return jsonify(result), (200 if "id" in result else 404)


@bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = user_service.delete_user(user_id)
    return jsonify(result), (200 if result["message"] == "Пользователь удалён" else 404)


    






app/routes/pet_routes.py:

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


    




app/routes/post_routes.py:

from flask import Blueprint, jsonify, request
from app.services import chat_service



bp = Blueprint('chat', __name__)


@bp.route('/chats', methods=['GET'])
def get_chats():
    chats = chat_service.get_all_chats()
    return jsonify(chats), 200


@bp.route('/chats/<int:chat_id>/message', methods=['POST'])
def send_message(chat_id):
    data = request.get_json()
    user_id = data.get('user_id')
    message = data.get('message')
    result = chat_service.send_message(chat_id, user_id, message)
    return jsonify(result), 201


@bp.route('/posts', methods=['GET'])
def get_posts():
    return jsonify({"message": "Посты пока не реализованы"}), 200

    






app/routes/user_routes.py:

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

    








app/services/__init__.py:

# пусто


app/services/auth_service.py:

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

    





app/services/chat_service.py:

def get_all_chats():
    return {"message": "Тут будут все чаты"}


def send_message(chat_id, user_id, message):
    return {"message": f"Сообщение в чат {chat_id} от юзера {user_id}: {message}"}

    





app/services/pet_service.py:

def get_pets():
    return {"pets": []}


def add_pet(owner_id, pet_data):
    return {
        "message": f"Питомец добавлен для владельца {owner_id}",
        "data": pet_data
    }

    




app/services/user_service.py:

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
        return False
    db.session.delete(user)
    db.session.commit()
    return True

    






app/utils/__init__.py:

# Пусто


app/utils/constants.py:

# Пусто


app/utils/helpers.py:

# Пусто


app/utils/validators.py:

# Пусто


app/extensions.py:

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()



app/__init__.py:

import os
from flask import Flask
from .extensions import db, migrate, jwt
from .routes import user_bp, auth_bp
from dotenv import load_dotenv



def create_app():
    app = Flask(__name__)
    load_dotenv()

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config.from_object('app.config.development.DevelopmentConfig')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')

    @app.route('/')
    def index():
        return {"message": "Main page is working here!!!"}

    return app

    

app/main.py:

# Пусто


tests/__init__.py:

# Пусто

tests/test_pets.py:

# Пусто

tests/test_users.py:

# Пусто



./run.py:

from app import create_app



app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

    


'''