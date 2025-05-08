from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv



load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
