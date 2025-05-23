from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user
from app.models import Jogador

auth_page = Blueprint('auth_page', __name__, template_folder='templates')

@auth_page.route('/login', methods=['GET', 'POST'])
def login():
    """
    Se o usuário não estiver autenticado, esta página sempre será solicitada.
    """
    if request.method == 'POST':
        cpf = request.form.get('cpf')
        jogador = Jogador.query.get(cpf)
        if jogador:
            login_user(jogador)
            return redirect(url_for('main.index'))
        flash('CPF não encontrado.', 'error')
    return render_template('login.html')