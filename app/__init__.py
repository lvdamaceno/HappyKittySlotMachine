from flask import Flask
from app.extensions import db, migrate, login_manager
from app.auth_page import auth_page
from app.auth_api import auth_api
from app.data_api import data_api
from app.views import main_bp

def create_app(config_object='config.Config'):
    # Configura caminhos de templates e estáticos
    app = Flask(
        __name__,
        template_folder='app/templates',
        static_folder='../static',
        static_url_path='/static'
    )
    app.config.from_object(config_object)

    # Inicializa extensões
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Registra blueprints
    app.register_blueprint(auth_page)
    app.register_blueprint(auth_api)
    app.register_blueprint(data_api)
    app.register_blueprint(main_bp)

    return app