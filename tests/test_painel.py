"""Testes do painel inicial, dos portlets e da busca global."""

from app import db
from app.models.cliente import Cliente
from app.models.contato import Contato
from tests.conftest import dados_cliente


def _semear(client_logado):
    """Cria uma base pequena com situacoes variadas para os portlets."""
    empresa = Cliente(
        tipo_pessoa="J",
        nome="ACME Industria Ltda",
        nome_fantasia="ACME",
        documento="11222333000181",
        email="contato@acme.com",
        telefone="1130001000",
    )
    pessoa_sem_dados = Cliente(
        tipo_pessoa="F", nome="Joao Pereira", documento="16899535009"
    )
    inativo = Cliente(
        tipo_pessoa="F",
        nome="Maria Silva",
        documento="52998224725",
        email="maria@exemplo.com",
        telefone="11912345678",
        ativo=False,
    )
    db.session.add_all([empresa, pessoa_sem_dados, inativo])
    db.session.commit()

    db.session.add(Contato(cliente_id=empresa.id, nome="Ana Souza", cargo="Diretora"))
    db.session.commit()

    return empresa, pessoa_sem_dados, inativo


class TestPainel:
    def test_painel_monta_os_quatro_portlets(self, client_logado):
        corpo = client_logado.get("/").get_data(as_text=True)

        assert 'data-portlet="configuracoes"' in corpo
        assert 'data-portlet="lembretes"' in corpo
        assert 'data-portlet="resumo_clientes"' in corpo
        assert 'data-portlet="ultimos_cadastros"' in corpo

    def test_barra_de_modulos_e_busca_aparecem_para_quem_esta_logado(self, client_logado):
        corpo = client_logado.get("/").get_data(as_text=True)

        assert "barra-modulos" in corpo
        assert "topo-busca" in corpo
        assert "Usuario de Teste" in corpo

    def test_tela_de_login_nao_mostra_a_barra_de_modulos(self, client):
        corpo = client.get("/auth/login").get_data(as_text=True)
        assert "barra-modulos" not in corpo


class TestPortletLembretes:
    def test_conta_clientes_sem_contato(self, app, client_logado):
        _semear(client_logado)

        from app.portlets import _dados_lembretes

        # Os lembretes montam links com url_for, entao precisam de um
        # contexto de requisicao ativo.
        with app.test_request_context():
            itens = _dados_lembretes()["itens"]

        # ACME tem contato; Joao Pereira nao. Maria esta inativa e nao conta.
        assert itens[0]["contagem"] == 1

    def test_conta_cadastros_incompletos_e_inativos(self, app, client_logado):
        _semear(client_logado)

        from app.portlets import _dados_lembretes

        with app.test_request_context():
            itens = _dados_lembretes()["itens"]

        assert itens[1]["contagem"] == 1  # Joao Pereira, sem e-mail e telefone
        assert itens[2]["contagem"] == 1  # Maria Silva, inativada

    def test_lembrete_zerado_nao_vira_link(self, client_logado):
        corpo = client_logado.get("/").get_data(as_text=True)
        assert "clientes inativados" in corpo


class TestPortletResumo:
    def test_totaliza_por_tipo_de_pessoa_e_situacao(self, client_logado):
        _semear(client_logado)

        from app.portlets import _dados_resumo_clientes

        dados = _dados_resumo_clientes()
        por_codigo = {linha["codigo"]: linha for linha in dados["linhas"]}

        assert por_codigo["J"]["ativos"] == 1
        assert por_codigo["J"]["contatos"] == 1
        assert por_codigo["F"]["ativos"] == 1
        assert por_codigo["F"]["inativos"] == 1
        assert dados["totais"]["total"] == 3


class TestBuscaGlobal:
    def test_termo_curto_nao_devolve_resultado(self, client_logado):
        _semear(client_logado)
        resposta = client_logado.get("/busca?q=a", headers={"HX-Request": "true"})

        assert resposta.status_code == 200
        assert "ACME" not in resposta.get_data(as_text=True)

    def test_encontra_cliente_por_nome(self, client_logado):
        _semear(client_logado)
        corpo = client_logado.get("/busca?q=acme").get_data(as_text=True)

        assert "ACME Industria Ltda" in corpo
        assert "Clientes" in corpo

    def test_encontra_cliente_por_documento_com_mascara(self, client_logado):
        _semear(client_logado)
        corpo = client_logado.get("/busca?q=11.222.333").get_data(as_text=True)

        assert "ACME Industria Ltda" in corpo

    def test_encontra_contato_e_mostra_o_cliente(self, client_logado):
        _semear(client_logado)
        corpo = client_logado.get("/busca?q=ana").get_data(as_text=True)

        assert "Ana Souza" in corpo
        assert "ACME Industria Ltda" in corpo

    def test_sem_resultado(self, client_logado):
        _semear(client_logado)
        corpo = client_logado.get("/busca?q=inexistente").get_data(as_text=True)

        assert "Nada encontrado" in corpo

    def test_busca_exige_autenticacao(self, client):
        resposta = client.get("/busca?q=acme")
        assert resposta.status_code == 302


class TestFiltrosDaListagem:
    def test_filtro_sem_contato(self, client_logado):
        _semear(client_logado)
        corpo = client_logado.get("/clientes/?filtro=sem_contato").get_data(as_text=True)

        assert "Joao Pereira" in corpo
        assert "ACME Industria Ltda" not in corpo

    def test_filtro_incompleto(self, client_logado):
        _semear(client_logado)
        corpo = client_logado.get("/clientes/?filtro=incompleto").get_data(as_text=True)

        assert "Joao Pereira" in corpo
        assert "ACME Industria Ltda" not in corpo

    def test_filtro_por_tipo_de_pessoa(self, client_logado):
        _semear(client_logado)
        corpo = client_logado.get("/clientes/?tipo=J").get_data(as_text=True)

        assert "ACME Industria Ltda" in corpo
        assert "Joao Pereira" not in corpo

    def test_filtro_aparece_no_subtitulo_com_opcao_de_limpar(self, client_logado):
        _semear(client_logado)
        corpo = client_logado.get("/clientes/?filtro=sem_contato").get_data(as_text=True)

        assert "Exibindo clientes ativos sem contato cadastrado" in corpo
        assert "limpar filtro" in corpo

    def test_filtro_sobrevive_a_busca_via_htmx(self, client_logado):
        _semear(client_logado)
        resposta = client_logado.get(
            "/clientes/?filtro=sem_contato&busca=Joao", headers={"HX-Request": "true"}
        )
        corpo = resposta.get_data(as_text=True)

        assert 'id="tabela-clientes"' in corpo
        assert "Joao Pereira" in corpo


class TestListagemDeContatos:
    def test_lista_todos_os_contatos(self, client_logado):
        _semear(client_logado)
        corpo = client_logado.get("/contatos").get_data(as_text=True)

        assert "Ana Souza" in corpo
        assert "ACME Industria Ltda" in corpo

    def test_busca_por_nome_do_cliente(self, client_logado):
        _semear(client_logado)
        resposta = client_logado.get(
            "/contatos?busca=acme", headers={"HX-Request": "true"}
        )
        corpo = resposta.get_data(as_text=True)

        assert 'id="tabela-contatos"' in corpo
        assert "Ana Souza" in corpo

    def test_busca_sem_resultado(self, client_logado):
        _semear(client_logado)
        corpo = client_logado.get("/contatos?busca=inexistente").get_data(as_text=True)

        assert "Nenhum contato encontrado" in corpo

    def test_exige_autenticacao(self, client):
        assert client.get("/contatos").status_code == 302


def test_cliente_cadastrado_aparece_nos_ultimos_cadastros(client_logado):
    client_logado.post("/clientes/novo", data=dados_cliente(), follow_redirects=True)
    corpo = client_logado.get("/").get_data(as_text=True)

    assert "Maria Silva" in corpo
