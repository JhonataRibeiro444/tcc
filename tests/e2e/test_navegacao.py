"""E2E: login, navegação e busca global (#30)."""

import re

import pytest
from playwright.sync_api import expect

from tests.e2e.conftest import EMAIL

pytestmark = pytest.mark.e2e


def test_login_abre_o_painel_com_os_quatro_portlets(logado):
    for titulo in [
        "Configuracoes rapidas",
        "Lembretes",
        "Resumo da base de clientes",
        "Ultimos cadastros",
    ]:
        expect(logado.get_by_text(titulo, exact=True)).to_be_visible()
    expect(logado.get_by_text(EMAIL)).to_be_visible()


def test_senha_errada_mostra_mensagem(page):
    page.goto("/auth/login")
    page.get_by_label("E-mail").fill(EMAIL)
    page.get_by_label("Senha").fill("errada")
    page.get_by_role("button", name="Entrar").click()

    expect(page.get_by_text("E-mail ou senha incorretos.")).to_be_visible()


def test_logout_volta_ao_login(logado):
    logado.get_by_role("link", name="Encerrar sessao").click()

    expect(logado).to_have_url(re.compile(r"/auth/login$"))
    logado.goto("/clientes/")
    expect(logado).to_have_url(re.compile(r"/auth/login"))


def test_busca_global_mostra_cliente_e_contato_enquanto_digita(logado, criar_cliente):
    criar_cliente(nome="Padaria Aurora", contatos=[{"nome": "Bruno Aurelio"}])
    logado.reload()

    logado.get_by_placeholder("Buscar clientes e contatos...").press_sequentially("Aur")

    resultados = logado.locator(".busca-item")
    expect(resultados.filter(has_text="Padaria Aurora").first).to_be_visible()
    expect(resultados.filter(has_text="Bruno Aurelio")).to_be_visible()


def test_lembrete_leva_a_lista_filtrada(logado, criar_cliente):
    criar_cliente(nome="Sem Contato Ltda")
    logado.reload()

    logado.get_by_role("link", name="clientes ativos sem contato cadastrado").click()

    expect(logado).to_have_url(re.compile(r"filtro=sem_contato"))
    expect(logado.get_by_role("link", name="Sem Contato Ltda")).to_be_visible()
