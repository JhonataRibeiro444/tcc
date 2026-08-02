from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()


def create_app(config_name="default"):
    app = Flask(
        __name__,
        template_folder="views/templates",
        static_folder="static",
    )
    app.config.from_object(config[config_name])

    db.init_app(app)

    # Registro dos Controllers (Blueprints)
    from app.controllers.main_controller import main_bp
    app.register_blueprint(main_bp)

    return app
