import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Configuracoes base da aplicacao."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "troque-esta-chave-em-producao")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(basedir, 'app.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Quantidade de registros por pagina nas listagens.
    ITENS_POR_PAGINA = 10


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    """Banco em memoria e CSRF desligado para os testes automatizados."""

    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
