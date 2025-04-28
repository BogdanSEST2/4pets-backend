from .auth_routes import bp as auth_bp
from .user_routes import bp as user_bp
from .pet_routes import bp as pet_bp
from .chat_routes import bp as chat_bp
from .post_routes import bp as post_bp


__all__ = ['auth_bp', 'user_bp', 'pet_bp', 'chat_bp', 'post_bp']
