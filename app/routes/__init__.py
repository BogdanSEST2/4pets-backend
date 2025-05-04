from .auth_routes import bp as auth_bp
from .user_routes import bp as user_bp
from .pet_routes import bp as pet_bp
from .chat_routes import bp as chat_bp
from .post_routes import bp as post_bp



__all__ = ['auth_bp', 'user_bp', 'pet_bp', 'chat_bp', 'post_bp']


def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(pet_bp, url_prefix='/pet')
    app.register_blueprint(chat_bp, url_prefix='/chat', name='chat_blueprint')
    app.register_blueprint(post_bp, url_prefix='/post', name='post_blueprint')
