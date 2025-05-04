from app import create_app, db
from flask_jwt_extended import JWTManager
from app.services.token_blacklist import blacklist



app = create_app()
jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return jwt_payload["jti"] in blacklist

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
