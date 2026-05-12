from models import db, login_manager
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20))  # child, parent, admin

    # Relationships
    child = db.relationship('Child', backref='user', uselist=False)
    parent = db.relationship('Parent', backref='user', uselist=False)
    admin = db.relationship('Admin', backref='user', uselist=False)

    def get_id(self):
        return str(self.id)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))