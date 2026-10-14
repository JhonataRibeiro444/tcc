from app import db
from app.models.cliente import Cliente
from tests.conftest import dados_cliente


def test_cadastra_cliente_valido(client_logado, app):
    resposta = client_logado.post(
        "/clientes/novo", data=dados_cliente(), follow_redirects=True
    )
    assert resposta.status_code == 200

    cliente = Cliente.query.filter_by(documento="52998224725").first()
    assert cliente is not None
    assert cliente.nome == "Maria Silva"
    # O documento e o telefone sao guardados sem pontuacao.
    assert cliente.telefone == "11912345678"


def test_recusa_cpf_invalido(client_logado):
    resposta = client_logado.post(
        "/clientes/novo", data=dados_cliente(documento="111.111.111-11")
    )
    assert "CPF invalido" in resposta.get_data(as_text=True)
    assert Cliente.query.count() == 0


def test_recusa_documento_duplicado(client_logado):
    client_logado.post("/clientes/novo", data=dados_cliente(), follow_redirects=True)
    resposta = client_logado.post(
        "/clientes/novo", data=dados_cliente(nome="Outro Nome")
    )
    assert "Ja existe um cliente cadastrado com este documento" in resposta.get_data(
        as_text=True
    )
    assert Cliente.query.count() == 1


def test_edicao_mantem_o_proprio_documento(client_logado):
    client_logado.post("/clientes/novo", data=dados_cliente(), follow_redirects=True)
    cliente = Cliente.query.first()

    resposta = client_logado.post(
        f"/clientes/{cliente.id}/editar",
        data=dados_cliente(nome="Maria Silva Souza"),
        follow_redirects=True,
    )
    assert resposta.status_code == 200
    assert db.session.get(Cliente, cliente.id).nome == "Maria Silva Souza"


def test_inativar_preserva_o_registro(client_logado):
    client_logado.post("/clientes/novo", data=dados_cliente(), follow_redirects=True)
    cliente = Cliente.query.first()

    client_logado.post(f"/clientes/{cliente.id}/situacao", follow_redirects=True)

    assert Cliente.query.count() == 1
    assert db.session.get(Cliente, cliente.id).ativo is False


def test_busca_htmx_devolve_somente_a_tabela(client_logado):
    client_logado.post("/clientes/novo", data=dados_cliente(), follow_redirects=True)

    resposta = client_logado.get(
        "/clientes/?busca=Maria", headers={"HX-Request": "true"}
    )
    corpo = resposta.get_data(as_text=True)

    assert "Maria Silva" in corpo
    assert 'id="tabela-clientes"' in corpo
    assert "<nav class=\"navbar" not in corpo


def test_busca_sem_resultado(client_logado):
    client_logado.post("/clientes/novo", data=dados_cliente(), follow_redirects=True)

    resposta = client_logado.get(
        "/clientes/?busca=inexistente", headers={"HX-Request": "true"}
    )
    assert "Nenhum cliente encontrado" in resposta.get_data(as_text=True)


def test_cliente_inexistente_responde_404(client_logado):
    assert client_logado.get("/clientes/999").status_code == 404
    assert client_logado.get("/clientes/999/editar").status_code == 404
    assert client_logado.post("/clientes/999/situacao").status_code == 404


def test_tela_de_edicao_mostra_documento_e_telefone_com_mascara(client_logado):
    client_logado.post("/clientes/novo", data=dados_cliente(), follow_redirects=True)
    cliente = Cliente.query.first()

    html = client_logado.get(f"/clientes/{cliente.id}/editar").get_data(as_text=True)

    assert "529.982.247-25" in html
    assert "(11) 91234-5678" in html


def test_edicao_com_cpf_invalido_nao_grava(client_logado):
    client_logado.post("/clientes/novo", data=dados_cliente(), follow_redirects=True)
    cliente = Cliente.query.first()

    resposta = client_logado.post(
        f"/clientes/{cliente.id}/editar", data=dados_cliente(documento="111.111.111-11")
    )

    assert resposta.status_code == 200
    assert db.session.get(Cliente, cliente.id).documento == "52998224725"


def test_reativar_cliente_inativado(client_logado):
    client_logado.post("/clientes/novo", data=dados_cliente(), follow_redirects=True)
    cliente = Cliente.query.first()

    client_logado.post(f"/clientes/{cliente.id}/situacao")
    client_logado.post(f"/clientes/{cliente.id}/situacao")

    assert db.session.get(Cliente, cliente.id).ativo is True
