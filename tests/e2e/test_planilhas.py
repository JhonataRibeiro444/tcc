"""E2E: fluxo completo de importação e exportação de planilhas (#32)."""

import csv
import io
import re

import openpyxl
import pytest
from playwright.sync_api import expect

from app.utils.planilhas import COLUNAS

pytestmark = pytest.mark.e2e


def _csv(caminho, *linhas):
    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=COLUNAS)
        escritor.writeheader()
        for linha in linhas:
            escritor.writerow({coluna: "" for coluna in COLUNAS} | linha)
    return caminho


def _baixar(page, acao):
    with page.expect_download() as download:
        acao()
    return download.value.path()


def test_importacao_completa(logado, criar_cliente, tmp_path):
    criar_cliente(nome="Ja Existe", documento="52998224725")
    planilha = _csv(
        tmp_path / "clientes.csv",
        {"tipo_pessoa": "F", "nome": "Nova Cliente", "documento": "111.444.777-35",
         "contato_nome": "Contato Principal"},
        {"tipo_pessoa": "F", "nome": "Duplicada", "documento": "529.982.247-25"},
        {"tipo_pessoa": "F", "nome": "Com Erro", "documento": "111.111.111-11"},
    )
    logado.goto("/clientes/importar")

    modelo = _baixar(logado, lambda: logado.get_by_role("link", name="Baixar planilha modelo").click())
    assert [c.value for c in openpyxl.load_workbook(io.BytesIO(modelo.read_bytes())).active[1]] == COLUNAS

    logado.get_by_label("Planilha (.xlsx ou .csv)").set_input_files(planilha)
    logado.get_by_role("button", name="Enviar e pre-visualizar").click()

    for total in ["1 pronto(s) para importar", "1 ja cadastrado(s)", "1 com erro"]:
        expect(logado.get_by_text(re.compile(rf"^\s*{re.escape(total)}\s*$"))).to_have_count(1)

    relatorio = _baixar(logado, lambda: logado.get_by_role("link", name="Baixar linhas nao importadas").click())
    texto = relatorio.read_text(encoding="utf-8-sig")
    assert "CPF invalido." in texto and "Documento ja cadastrado." in texto

    logado.get_by_role("button", name=re.compile("Confirmar importacao de 1 cliente")).click()

    expect(logado).to_have_url(re.compile(r"/clientes/$"))
    expect(logado.get_by_text("1 cliente(s) importado(s).")).to_be_visible()
    expect(logado.get_by_role("link", name="Nova Cliente")).to_be_visible()
    expect(logado.get_by_role("link", name="Com Erro")).to_have_count(0)


def test_exportacao_respeita_o_filtro(logado, criar_cliente):
    criar_cliente(nome="Ativa Exportada", documento="52998224725")
    criar_cliente(nome="Inativa Fora", documento="11144477735", ativo=False)
    logado.goto("/clientes/?situacao=ativos")

    logado.get_by_role("button", name="Planilha").click()
    arquivo = _baixar(logado, lambda: logado.get_by_role("link", name="Exportar (.csv)").click())

    texto = arquivo.read_text(encoding="utf-8-sig")
    assert "Ativa Exportada" in texto
    assert "Inativa Fora" not in texto
