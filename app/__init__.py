from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import config

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

login_manager.login_view = "auth.login"
login_manager.login_message = "Faca login para acessar esta pagina."
login_manager.login_message_category = "warning"


def create_app(config_name="default"):
    app = Flask(
        __name__,
        template_folder="views/templates",
        static_folder="static",
    )
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Os models precisam ser importados antes do create_all/user_loader.
    from app.models.usuario import Usuario

    @login_manager.user_loader
    def carregar_usuario(usuario_id):
        return db.session.get(Usuario, int(usuario_id))

    # Registro dos Controllers (Blueprints)
    from app.controllers.auth_controller import auth_bp
    from app.controllers.cliente_controller import cliente_bp
    from app.controllers.contato_controller import contato_bp
    from app.controllers.main_controller import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(contato_bp)

    from app.cli import registrar_comandos

    registrar_comandos(app)

    return app
