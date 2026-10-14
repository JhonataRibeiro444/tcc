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


HTMX = {"HX-Request": "true"}


def _criar_contato(client_logado, cliente, **dados):
    client_logado.post(
        f"/clientes/{cliente.id}/contatos", data={"nome": "Base", **dados}, headers=HTMX
    )
    return Contato.query.order_by(Contato.id.desc()).first()


def test_abrir_e_cancelar_formulario_via_htmx(client_logado):
    cliente = _criar_cliente(client_logado)

    aberto = client_logado.get(f"/clientes/{cliente.id}/contatos/novo", headers=HTMX)
    fechado = client_logado.get(f"/clientes/{cliente.id}/contatos/cancelar", headers=HTMX)

    assert "<form" in aberto.get_data(as_text=True)
    assert "<form" not in fechado.get_data(as_text=True)


def test_editar_abre_formulario_preenchido(client_logado):
    cliente = _criar_cliente(client_logado)
    contato = _criar_contato(client_logado, cliente, nome="Ana Lima", telefone="11912345678")

    html = client_logado.get(f"/contatos/{contato.id}/editar", headers=HTMX).get_data(
        as_text=True
    )

    assert f"/contatos/{contato.id}/editar" in html
    assert "Ana Lima" in html
    assert "(11) 91234-5678" in html


def test_editar_contato_grava_alteracao(client_logado):
    cliente = _criar_cliente(client_logado)
    contato = _criar_contato(client_logado, cliente)

    client_logado.post(
        f"/contatos/{contato.id}/editar",
        data={"nome": "Nome Novo", "cargo": "Diretor", "telefone": "(11) 3333-4444"},
        headers=HTMX,
    )

    editado = db.session.get(Contato, contato.id)
    assert (editado.nome, editado.cargo, editado.telefone) == ("Nome Novo", "Diretor", "1133334444")


def test_editar_contato_sem_nome_e_recusado(client_logado):
    cliente = _criar_cliente(client_logado)
    contato = _criar_contato(client_logado, cliente, nome="Original")

    resposta = client_logado.post(
        f"/contatos/{contato.id}/editar", data={"nome": ""}, headers=HTMX
    )

    assert "Informe o nome do contato" in resposta.get_data(as_text=True)
    assert db.session.get(Contato, contato.id).nome == "Original"


def test_tornar_principal_na_edicao_desmarca_o_anterior(client_logado):
    cliente = _criar_cliente(client_logado)
    antigo = _criar_contato(client_logado, cliente, nome="Antigo", principal="y")
    novo = _criar_contato(client_logado, cliente, nome="Novo")

    client_logado.post(
        f"/contatos/{novo.id}/editar", data={"nome": "Novo", "principal": "y"}, headers=HTMX
    )

    assert db.session.get(Contato, novo.id).principal is True
    assert db.session.get(Contato, antigo.id).principal is False


def test_acoes_sem_htmx_redirecionam_ao_cliente(client_logado):
    cliente = _criar_cliente(client_logado)

    resposta = client_logado.post(f"/clientes/{cliente.id}/contatos", data={"nome": "Sem HTMX"})

    assert resposta.status_code == 302
    assert resposta.headers["Location"] == f"/clientes/{cliente.id}"


def test_contato_inexistente_responde_404(client_logado):
    assert client_logado.get("/contatos/999/editar", headers=HTMX).status_code == 404
    assert client_logado.post("/contatos/999/excluir", headers=HTMX).status_code == 404


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
