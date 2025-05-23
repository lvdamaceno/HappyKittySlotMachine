from flask import Blueprint, request, jsonify, current_app
from app.models import Jogador, Pontos, Jogadas
from app.extensions import db

data_api = Blueprint('data_api', __name__, url_prefix='/api')

@data_api.route('/players', methods=['POST'])
def add_or_update_player():
    data = request.get_json() or {}
    cpf = data.get('cpf')
    name = data.get('name')
    pontos_val = data.get('pontos')
    jogadas_val = data.get('jogadas')

    if not cpf:
        return jsonify({'error': 'CPF é obrigatório.'}), 400

    jogador = Jogador.query.get(cpf)
    if not jogador:
        if not name:
            return jsonify({'error': 'Nome é obrigatório para novo jogador.'}), 400
        jogador = Jogador(cpf=cpf, name=name)
        db.session.add(jogador)
    elif name:
        jogador.name = name

    pontos = Pontos.query.get(cpf)
    if pontos and pontos_val is not None:
        pontos.pontos = pontos_val
    elif not pontos:
        pontos = Pontos(
            cpf=cpf,
            pontos=pontos_val if pontos_val is not None else current_app.config['STARTING_COINS']
        )
        db.session.add(pontos)

    jog = Jogadas.query.get(cpf)
    if jog and jogadas_val is not None:
        jog.jogadas = jogadas_val
    elif not jog:
        jog = Jogadas(
            cpf=cpf,
            jogadas=jogadas_val if jogadas_val is not None else current_app.config['MAX_ATTEMPTS']
        )
        db.session.add(jog)

    db.session.commit()
    return jsonify({'message': 'Jogador e pontos atualizados.', 'cpf': cpf}), 200