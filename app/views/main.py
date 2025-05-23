from flask import Blueprint, render_template, session, current_app, jsonify
from app.extensions import db, login_manager
from app.models import User
from app.services import GameService

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    user_id = session.get('user_id')
    user = None

    if user_id:
        user = User.query.get(user_id)

    if user is None:
        session.pop('user_id', None)
        user = User(
            coins=current_app.config['STARTING_COINS'],
            attempts=current_app.config['MAX_ATTEMPTS']
        )
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id

    return render_template('index.html', coins=user.coins, attempts=user.attempts)

@main_bp.route('/spin', methods=['POST'])
def spin():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'Sessão expirada. Recarregue a página.'}), 400

    results, reward = GameService.spin(user)
    return jsonify({
        'figures':  results,
        'coins':    user.coins,
        'attempts': user.attempts,
        'reward':   reward
    })