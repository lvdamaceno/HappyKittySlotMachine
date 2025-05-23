from flask import Blueprint, render_template, jsonify, redirect, url_for, current_app
from flask_login import login_required, current_user
from app.services import GameService
from app.models import Pontos, Jogadas

main_bp = Blueprint('main', __name__, template_folder='templates')

@main_bp.route('/')
@login_required
def index():
    # Carrega DO BANCO
    pts = Pontos.query.get(current_user.cpf)
    jg = Jogadas.query.get(current_user.cpf)
    if pts is None or jg is None:
    # redireciona ou dá erro, mas não recria defaults!
        return redirect(url_for('auth_page.login'))
    return render_template('index.html',coins=pts.pontos,attempts = jg.jogadas)


@main_bp.route('/spin', methods=['POST'])
@login_required
def spin():
    current_app.logger.info(f"→ Rota /spin RECEBIDA para CPF={current_user.cpf}")
    print(f"→ Rota /spin RECEBIDA para CPF={current_user.cpf}", flush=True)
    # Executa o spin e já grava no banco via GameService
    results, reward, error = GameService.spin(current_user.cpf)
    if error:
        return jsonify({'error': error}), 400

    # Busca NOVAMENTE para refletir valores atualizados
    pts = Pontos.query.get(current_user.cpf)
    jg  = Jogadas.query.get(current_user.cpf)
    return jsonify({
        'figures':  results,
        'coins':    pts.pontos,
        'attempts': jg.jogadas,
        'reward':   reward
    })