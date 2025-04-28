import os
from flask import Flask
from .extensions import db, migrate, jwt
from dotenv import load_dotenv
from .routes import user_bp, auth_bp, pet_bp




def create_app():
    app = Flask(__name__)
    load_dotenv()

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///dev_db.sqlite3')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key')
    app.config.from_object('app.config.development.DevelopmentConfig')
    

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(pet_bp, url_prefix='/pet')

    @app.route('/')
    def index():
        return {"message": "Main page is working here!!!"}

    return app


