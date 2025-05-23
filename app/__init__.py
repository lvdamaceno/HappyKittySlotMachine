import logging
import os
from logging.handlers import RotatingFileHandler

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
        template_folder='templates',
        static_folder='static',
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


    if not app.debug:
        log_dir = os.path.join(os.getcwd(), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        file_handler = RotatingFileHandler(
            os.path.join(log_dir, 'app.log'),
            maxBytes=10*1024*1024,
            backupCount=5
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        app.logger.addHandler(file_handler)


    return app

