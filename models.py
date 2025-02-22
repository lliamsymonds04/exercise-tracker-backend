from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    passwordHash = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'