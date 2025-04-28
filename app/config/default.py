from .config import Config



class DefaultConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///default_db.sqlite3'
