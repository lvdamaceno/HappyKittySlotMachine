from flask_login import UserMixin
from app.extensions import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    coins = db.Column(db.Integer, nullable=False)
    attempts = db.Column(db.Integer, nullable=False)

class PointTransaction(db.Model):
    __tablename__ = 'point_transactions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    change = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    user = db.relationship('User', backref='transactions')