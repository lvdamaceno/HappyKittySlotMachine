from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
# Página de login para usuários não autenticados
login_manager.login_view = 'auth_page.login'

@login_manager.user_loader
def load_user(cpf):
    from app.models import Jogador
    return Jogador.query.get(cpf)