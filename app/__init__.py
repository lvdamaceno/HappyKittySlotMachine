from flask import Flask
from app.extensions import db, migrate, login_manager
from app.views.main import main_bp


def create_app(config_object='config.Config'):
    # informa ao Flask onde estão os assets
    app = Flask(
        __name__,
        static_folder='../static',       # pasta “static/” na raiz do projeto
        template_folder='templates'      # ‘app/templates/’
    )
    app.config.from_object(config_object)

    from app.extensions import db, migrate, login_manager
    from app.views.main    import main_bp

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    app.register_blueprint(main_bp)
    return app
