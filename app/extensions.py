from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Instâncias globais para lazy initialization
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.index'

# Callback para carregar usuário a partir de session (Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))