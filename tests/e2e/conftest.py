"""Infraestrutura dos testes end-to-end: a aplicacao roda num servidor real,
com banco SQLite temporario e CSRF ligado, e o Playwright a usa pelo navegador.

Rodar com: python -m pytest -m e2e --no-cov
"""

import threading

import pytest
from werkzeug.serving import make_server

from app import create_app, db
from app.models.usuario import Usuario
from config import Config, config

EMAIL = "e2e@exemplo.com"
SENHA = "senha-e2e"


@pytest.fixture(scope="session")
def servidor(tmp_path_factory):
    banco = tmp_path_factory.mktemp("e2e") / "app.db"
    config["e2e"] = type(
        "E2EConfig", (Config,), {"SQLALCHEMY_DATABASE_URI": f"sqlite:///{banco}"}
    )
    app = create_app("e2e")
    with app.app_context():
        db.create_all()
        usuario = Usuario(nome="Usuario E2E", email=EMAIL)
        usuario.definir_senha(SENHA)
        db.session.add(usuario)
        db.session.commit()

    http = make_server("127.0.0.1", 0, app, threaded=True)
    threading.Thread(target=http.serve_forever, daemon=True).start()
    yield app, f"http://127.0.0.1:{http.server_port}"
    http.shutdown()


@pytest.fixture(scope="session")
def base_url(servidor):
    return servidor[1]


@pytest.fixture(autouse=True)
def banco_limpo(servidor):
    """Cada teste comeca so com o usuario E2E."""
    app = servidor[0]
    yield
    with app.app_context():
        for tabela in reversed(db.metadata.sorted_tables):
            if tabela.name != "usuarios":
                db.session.execute(tabela.delete())
        db.session.commit()


@pytest.fixture
def logado(page):
    page.goto("/auth/login")
    page.get_by_label("E-mail").fill(EMAIL)
    page.get_by_label("Senha").fill(SENHA)
    page.get_by_role("button", name="Entrar").click()
    page.wait_for_url("**/")
    return page
