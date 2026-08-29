import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db  # noqa: E402
from app.models.usuario import Usuario  # noqa: E402

SENHA_PADRAO = "senha-de-teste"


@pytest.fixture
def app():
    aplicacao = create_app("testing")

    with aplicacao.app_context():
        db.create_all()
        usuario = Usuario(nome="Usuario de Teste", email="teste@exemplo.com")
        usuario.definir_senha(SENHA_PADRAO)
        db.session.add(usuario)
        db.session.commit()

        yield aplicacao

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def client_logado(client):
    client.post(
        "/auth/login",
        data={"email": "teste@exemplo.com", "senha": SENHA_PADRAO},
        follow_redirects=True,
    )
    return client


def dados_cliente(**alteracoes):
    """Payload valido de cliente, com os campos que o formulario espera."""
    dados = {
        "tipo_pessoa": "F",
        "nome": "Maria Silva",
        "nome_fantasia": "",
        "documento": "529.982.247-25",
        "email": "maria@exemplo.com",
        "telefone": "(11) 91234-5678",
        "cep": "01001000",
        "logradouro": "Praca da Se",
        "numero": "100",
        "complemento": "",
        "bairro": "Se",
        "cidade": "Sao Paulo",
        "uf": "SP",
        "observacoes": "",
        "ativo": "y",
    }
    dados.update(alteracoes)
    return dados
