from app.extensions import db



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    messages = db.relationship('Message', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"
