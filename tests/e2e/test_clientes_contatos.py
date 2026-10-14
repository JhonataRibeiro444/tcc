"""E2E: cadastro com máscaras e painel de contatos (#31)."""

import re

import pytest
from playwright.sync_api import expect

from app.models.cliente import Cliente

pytestmark = pytest.mark.e2e


def _cliente_no_banco(servidor, nome):
    with servidor[0].app_context():
        return Cliente.query.filter_by(nome=nome).one()


def test_mascaras_formatam_durante_a_digitacao(logado):
    logado.goto("/clientes/novo")

    logado.get_by_label("CPF / CNPJ").press_sequentially("52998224725")
    logado.get_by_label("Telefone").press_sequentially("11912345678")
    logado.get_by_label("CEP").press_sequentially("01001000")
    expect(logado.get_by_label("CPF / CNPJ")).to_have_value("529.982.247-25")
    expect(logado.get_by_label("Telefone")).to_have_value("(11) 91234-5678")
    expect(logado.get_by_label("CEP")).to_have_value("01001-000")

    logado.get_by_label("Tipo de pessoa").select_option("J")
    logado.get_by_label("CPF / CNPJ").fill("")
    logado.get_by_label("CPF / CNPJ").press_sequentially("11222333000181")
    expect(logado.get_by_label("CPF / CNPJ")).to_have_value("11.222.333/0001-81")


def test_cadastro_com_mascara_grava_so_digitos(logado, servidor):
    logado.goto("/clientes/novo")
    logado.get_by_label("Nome / Razao social").fill("Cliente Mascarado")
    logado.get_by_label("CPF / CNPJ").press_sequentially("52998224725")
    logado.get_by_label("Telefone").press_sequentially("11912345678")
    logado.get_by_role("button", name="Salvar").click()

    expect(logado.get_by_text("Cliente cadastrado com sucesso.")).to_be_visible()
    cliente = _cliente_no_banco(servidor, "Cliente Mascarado")
    assert (cliente.documento, cliente.telefone) == ("52998224725", "11912345678")


def test_cpf_invalido_mostra_erro_no_formulario(logado, servidor):
    logado.goto("/clientes/novo")
    logado.get_by_label("Nome / Razao social").fill("Cliente Invalido")
    logado.get_by_label("CPF / CNPJ").press_sequentially("11111111111")
    logado.get_by_role("button", name="Salvar").click()

    expect(logado).to_have_url(re.compile(r"/clientes/novo$"))
    expect(logado.get_by_text(re.compile("CPF invalido", re.I)).first).to_be_visible()
    with servidor[0].app_context():
        assert Cliente.query.filter_by(nome="Cliente Invalido").count() == 0


def test_busca_da_listagem_atualiza_sem_recarregar(logado, criar_cliente):
    criar_cliente(nome="Alfa Comercio", documento="52998224725")
    criar_cliente(nome="Beta Servicos", documento="11144477735")
    logado.goto("/clientes/")
    logado.evaluate("window.marcador = 'mesma-pagina'")

    logado.get_by_placeholder(re.compile("Buscar", re.I)).last.press_sequentially("Beta")

    expect(logado.get_by_role("link", name="Alfa Comercio")).to_be_hidden()
    expect(logado.get_by_role("link", name="Beta Servicos")).to_be_visible()
    assert logado.evaluate("window.marcador") == "mesma-pagina"


def test_painel_de_contatos_adiciona_edita_e_remove(logado, criar_cliente):
    cliente_id = criar_cliente(nome="Empresa Contatos")
    logado.goto(f"/clientes/{cliente_id}")
    logado.evaluate("window.marcador = 'mesma-pagina'")
    painel = logado.locator("#painel-contatos")

    painel.get_by_role("button", name="Novo contato").click()
    painel.get_by_label("Nome").fill("Carla Dias")
    painel.get_by_role("button", name="Salvar contato").click()
    expect(painel.get_by_text("Carla Dias")).to_be_visible()

    painel.get_by_role("button", name="Editar").click()
    painel.get_by_label("Nome").fill("Carla Dias Souza")
    painel.get_by_role("button", name="Salvar contato").click()
    expect(painel.get_by_text("Carla Dias Souza")).to_be_visible()

    logado.once("dialog", lambda dialogo: dialogo.accept())
    painel.get_by_role("button", name="Remover").click()
    expect(painel.get_by_text("Carla Dias Souza")).to_be_hidden()
    assert logado.evaluate("window.marcador") == "mesma-pagina"
