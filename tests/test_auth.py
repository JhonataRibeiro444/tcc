from tests.conftest import SENHA_PADRAO


def test_rota_protegida_redireciona_para_login(client):
    resposta = client.get("/")
    assert resposta.status_code == 302
    assert "/auth/login" in resposta.headers["Location"]


def test_login_com_senha_errada_nao_autentica(client):
    resposta = client.post(
        "/auth/login",
        data={"email": "teste@exemplo.com", "senha": "errada"},
        follow_redirects=True,
    )
    assert "E-mail ou senha incorretos" in resposta.get_data(as_text=True)


def test_login_valido_da_acesso_ao_painel(client):
    resposta = client.post(
        "/auth/login",
        data={"email": "teste@exemplo.com", "senha": SENHA_PADRAO},
        follow_redirects=True,
    )
    assert resposta.status_code == 200
    assert "Painel" in resposta.get_data(as_text=True)


def test_logout_encerra_a_sessao(client_logado):
    client_logado.get("/auth/logout", follow_redirects=True)
    resposta = client_logado.get("/")
    assert resposta.status_code == 302


def _entrar(client, next_=None):
    url = "/auth/login" + (f"?next={next_}" if next_ else "")
    return client.post(url, data={"email": "teste@exemplo.com", "senha": SENHA_PADRAO})


def test_login_segue_next_relativo(client):
    resposta = _entrar(client, "/clientes/")
    assert resposta.headers["Location"] == "/clientes/"


def test_login_ignora_next_externo(client):
    resposta = _entrar(client, "https://site-malicioso.com/")
    assert resposta.headers["Location"] == "/"


def test_conta_desativada_nao_entra(app, client):
    from app import db
    from app.models.usuario import Usuario

    Usuario.query.filter_by(email="teste@exemplo.com").one().ativo = False
    db.session.commit()

    resposta = client.post(
        "/auth/login",
        data={"email": "teste@exemplo.com", "senha": SENHA_PADRAO},
        follow_redirects=True,
    )
    assert "Este usuario esta desativado." in resposta.get_data(as_text=True)
    assert client.get("/").status_code == 302


def test_usuario_logado_que_abre_o_login_vai_ao_painel(client_logado):
    resposta = client_logado.get("/auth/login")
    assert resposta.status_code == 302
    assert resposta.headers["Location"] == "/"


def test_senha_nao_e_gravada_em_texto_puro(app):
    from app.models.usuario import Usuario

    usuario = Usuario.query.filter_by(email="teste@exemplo.com").first()
    assert usuario.senha_hash != SENHA_PADRAO
    assert usuario.verificar_senha(SENHA_PADRAO)
