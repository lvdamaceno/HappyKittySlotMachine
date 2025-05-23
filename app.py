from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Inicialização da app
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

# Exemplo de modelo para usuários e transações de moedas
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coins = db.Column(db.Integer, default=app.config['STARTING_COINS'])
    attempts = db.Column(db.Integer, default=app.config['MAX_ATTEMPTS'])

class PointTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    change = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

# Crie as tabelas com: flask shell -> db.create_all()

@app.route('/')
def index():
    # Aqui você pode buscar ou criar um usuário anônimo na sessão
    user_id = session.get('user_id')
    if not user_id:
        user = User()
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
    else:
        user = User.query.get(user_id)

    return render_template('index.html', coins=user.coins, attempts=user.attempts)

# Mais rotas para girar, registrar transações, etc.

if __name__ == '__main__':
    app.run(debug=True)