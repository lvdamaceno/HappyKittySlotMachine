from flask_login import UserMixin
from app.extensions import db
from datetime import datetime
from sqlalchemy import Enum

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

class RegistroJogada(db.Model):
    __tablename__ = 'registro_jogadas'

    id        = db.Column(db.Integer, primary_key=True)
    cpf       = db.Column(db.String(11), db.ForeignKey('jogadores.cpf'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    resultado = db.Column(Enum('ganhou', 'perder', name='resultado_enum'), nullable=False)
    quantidade= db.Column(db.Integer, nullable=False)