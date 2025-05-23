from flask_login import UserMixin
from app.extensions import db

class Jogador(UserMixin, db.Model):
    __tablename__ = 'jogadores'
    cpf = db.Column(db.String(11), primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def get_id(self):
        return self.cpf

class Pontos(db.Model):
    __tablename__ = 'pontos'
    cpf = db.Column(db.String(11), db.ForeignKey('jogadores.cpf'), primary_key=True)
    pontos = db.Column(db.Integer, nullable=False)

class Jogadas(db.Model):
    __tablename__ = 'jogadas'
    cpf = db.Column(db.String(11), db.ForeignKey('jogadores.cpf'), primary_key=True)
    jogadas = db.Column(db.Integer, nullable=False)