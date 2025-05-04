import os
from flask import Flask
from .extensions import db, migrate, jwt
from dotenv import load_dotenv
from app.routes import register_routes

def create_app(config_name=None):
    app = Flask(__name__)
    load_dotenv()

    if config_name == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SECRET_KEY'] = 'test_secret_key'
        app.config['JWT_SECRET_KEY'] = 'test_jwt_secret'
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///dev_db.sqlite3')
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
        app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key')
        app.config.from_object('app.config.development.DevelopmentConfig')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    register_routes(app)

    @app.route('/')
    def index():
        return {"message": "Main page is working here!!!"}

    return app
