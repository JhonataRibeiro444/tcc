from app import db
from app.models.cliente import Cliente
from app.models.contato import Contato
from tests.conftest import dados_cliente


def _criar_cliente(client_logado):
    client_logado.post("/clientes/novo", data=dados_cliente(), follow_redirects=True)
    return Cliente.query.first()


def test_adiciona_contato_ao_cliente(client_logado):
    cliente = _criar_cliente(client_logado)

    resposta = client_logado.post(
        f"/clientes/{cliente.id}/contatos",
        data={"nome": "Joao Souza", "cargo": "Comprador", "email": "joao@exemplo.com"},
        headers={"HX-Request": "true"},
    )

    assert resposta.status_code == 200
    assert 'id="painel-contatos"' in resposta.get_data(as_text=True)
    assert Contato.query.filter_by(nome="Joao Souza").count() == 1


def test_contato_sem_nome_e_recusado(client_logado):
    cliente = _criar_cliente(client_logado)

    resposta = client_logado.post(
        f"/clientes/{cliente.id}/contatos",
        data={"nome": "", "cargo": "Comprador"},
        headers={"HX-Request": "true"},
    )

    assert "Informe o nome do contato" in resposta.get_data(as_text=True)
    assert Contato.query.count() == 0


def test_apenas_um_contato_principal_por_cliente(client_logado):
    cliente = _criar_cliente(client_logado)

    client_logado.post(
        f"/clientes/{cliente.id}/contatos",
        data={"nome": "Primeiro", "principal": "y"},
        headers={"HX-Request": "true"},
    )
    client_logado.post(
        f"/clientes/{cliente.id}/contatos",
        data={"nome": "Segundo", "principal": "y"},
        headers={"HX-Request": "true"},
    )

    principais = Contato.query.filter_by(principal=True).all()
    assert len(principais) == 1
    assert principais[0].nome == "Segundo"


def test_remover_contato(client_logado):
    cliente = _criar_cliente(client_logado)
    client_logado.post(
        f"/clientes/{cliente.id}/contatos",
        data={"nome": "Temporario"},
        headers={"HX-Request": "true"},
    )
    contato = Contato.query.first()

    client_logado.post(
        f"/contatos/{contato.id}/excluir", headers={"HX-Request": "true"}
    )

    assert Contato.query.count() == 0


def test_excluir_cliente_remove_seus_contatos(client_logado):
    cliente = _criar_cliente(client_logado)
    client_logado.post(
        f"/clientes/{cliente.id}/contatos",
        data={"nome": "Vinculado"},
        headers={"HX-Request": "true"},
    )

    db.session.delete(db.session.get(Cliente, cliente.id))
    db.session.commit()

    assert Contato.query.count() == 0
