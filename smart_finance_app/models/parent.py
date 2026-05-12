from models import db

class Parent(db.Model):
    __tablename__ = 'parent'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # One parent → many children
    children = db.relationship('Child', backref='parent', lazy=True)