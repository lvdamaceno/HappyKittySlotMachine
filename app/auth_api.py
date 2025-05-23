from flask import Blueprint, request, jsonify
from flask_login import login_user
from app.models import Jogador, Pontos, Jogadas
from app.extensions import db
from flask import current_app

auth_api = Blueprint('auth_api', __name__, url_prefix='/api/auth')

@auth_api.route('/login', methods=['POST'])
def api_login():
    data = request.get_json() or {}
    cpf = data.get('cpf')
    jogador = Jogador.query.get(cpf)
    if not jogador:
        return jsonify({'error': 'CPF não cadastrado.'}), 404
    login_user(jogador)
    pts = Pontos.query.get(cpf)
    jg = Jogadas.query.get(cpf)
    return jsonify({'cpf': cpf, 'pontos': pts.pontos, 'jogadas': jg.jogadas}), 200

@auth_api.route('/register', methods=['POST'])
def api_register():
    data = request.get_json() or {}
    cpf      = data.get('cpf')
    name     = data.get('name')
    pontos_v = data.get('pontos')
    jogadas_v= data.get('jogadas')

    if not cpf or not name:
        return jsonify({'error': 'cpf e name são obrigatórios.'}), 400
    # Verifica se já existe
    if Jogador.query.get(cpf):
        return jsonify({'error': 'CPF já cadastrado.'}), 409

    # Seed usando os valores do JSON (sem fallback)
    jogador = Jogador(cpf=cpf, name=name)
    db.session.add(jogador)
    db.session.add(Pontos(cpf=cpf, pontos=pontos_v))
    db.session.add(Jogadas(cpf=cpf, jogadas=jogadas_v))
    db.session.commit()
    return jsonify({'message': 'Cadastro realizado.'}), 201