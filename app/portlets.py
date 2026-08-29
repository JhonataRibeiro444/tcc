"""Registro de portlets do painel inicial.

Um portlet e um bloco independente da tela inicial: tem um titulo, um
template proprio e uma funcao que busca os seus dados. Registrar um
portlet novo e acrescentar uma entrada aqui - o template do painel nao
precisa ser alterado.

O layout e fixo nesta versao (a coluna e a ordem vem do proprio
registro). Quando o painel configuravel pelo usuario for implementado,
basta uma tabela de preferencias que sobreponha `coluna` e `ordem`; a
estrutura abaixo ja foi pensada para isso.
"""

from dataclasses import dataclass, field
from typing import Callable

from flask import url_for

COLUNA_ESQUERDA = "esquerda"
COLUNA_DIREITA = "direita"


@dataclass(frozen=True)
class Portlet:
    chave: str
    titulo: str
    coluna: str
    template: str
    dados: Callable[[], dict]
    ordem: int = 0


_REGISTRO: dict[str, Portlet] = {}


def registrar(portlet: Portlet) -> Portlet:
    _REGISTRO[portlet.chave] = portlet
    return portlet


def listar(coluna: str) -> list[Portlet]:
    """Portlets de uma coluna, ja na ordem de exibicao."""
    da_coluna = [p for p in _REGISTRO.values() if p.coluna == coluna]
    return sorted(da_coluna, key=lambda p: (p.ordem, p.titulo))


def montar(coluna: str) -> list[dict]:
    """Executa as funcoes de dados dos portlets da coluna."""
    return [{"portlet": p, "dados": p.dados()} for p in listar(coluna)]


# =====================================================================
# Funcoes de dados
# =====================================================================


def _dados_configuracoes() -> dict:
    """Atalhos de uso frequente, no espirito do portlet de configuracoes."""
    return {
        "links": [
            {"rotulo": "Cadastrar novo cliente", "url": url_for("clientes.novo")},
            {"rotulo": "Todos os clientes", "url": url_for("clientes.listar")},
            {
                "rotulo": "Somente clientes ativos",
                "url": url_for("clientes.listar", situacao="ativos"),
            },
            {"rotulo": "Todos os contatos", "url": url_for("contatos.listar")},
            {"rotulo": "Encerrar sessao", "url": url_for("auth.logout")},
        ]
    }


def _dados_lembretes() -> dict:
    """Situacoes que merecem atencao do usuario, cada uma com o seu link."""
    from app import db
    from app.models.cliente import Cliente

    sem_contato = Cliente.query.filter(
        ~Cliente.contatos.any(), Cliente.ativo.is_(True)
    ).count()

    incompletos = Cliente.query.filter(
        Cliente.ativo.is_(True),
        db.or_(Cliente.email.is_(None), Cliente.telefone.is_(None)),
    ).count()

    inativos = Cliente.query.filter_by(ativo=False).count()

    return {
        "itens": [
            {
                "contagem": sem_contato,
                "descricao": "clientes ativos sem contato cadastrado",
                "url": url_for("clientes.listar", filtro="sem_contato"),
            },
            {
                "contagem": incompletos,
                "descricao": "clientes sem e-mail ou telefone",
                "url": url_for("clientes.listar", filtro="incompleto"),
            },
            {
                "contagem": inativos,
                "descricao": "clientes inativados",
                "url": url_for("clientes.listar", situacao="inativos"),
            },
        ]
    }


def _dados_resumo_clientes() -> dict:
    """Distribuicao da base por tipo de pessoa e situacao."""
    from app.models.cliente import TIPOS_PESSOA, Cliente
    from app.models.contato import Contato

    linhas = []
    for codigo, rotulo in TIPOS_PESSOA.items():
        ativos = Cliente.query.filter_by(tipo_pessoa=codigo, ativo=True).count()
        inativos = Cliente.query.filter_by(tipo_pessoa=codigo, ativo=False).count()
        contatos = (
            Contato.query.join(Cliente).filter(Cliente.tipo_pessoa == codigo).count()
        )
        linhas.append(
            {
                "codigo": codigo,
                "rotulo": rotulo,
                "ativos": ativos,
                "inativos": inativos,
                "total": ativos + inativos,
                "contatos": contatos,
            }
        )

    return {
        "linhas": linhas,
        "totais": {
            "ativos": sum(linha["ativos"] for linha in linhas),
            "inativos": sum(linha["inativos"] for linha in linhas),
            "total": sum(linha["total"] for linha in linhas),
            "contatos": sum(linha["contatos"] for linha in linhas),
        },
    }


def _dados_ultimos_cadastros() -> dict:
    from app.models.cliente import Cliente
    from app.models.contato import Contato

    return {
        "clientes": Cliente.query.order_by(Cliente.criado_em.desc()).limit(5).all(),
        "contatos": Contato.query.order_by(Contato.criado_em.desc()).limit(5).all(),
    }


# =====================================================================
# Registro
# =====================================================================

registrar(
    Portlet(
        chave="configuracoes",
        titulo="Configuracoes rapidas",
        coluna=COLUNA_ESQUERDA,
        template="portlets/_configuracoes.html",
        dados=_dados_configuracoes,
        ordem=10,
    )
)

registrar(
    Portlet(
        chave="lembretes",
        titulo="Lembretes",
        coluna=COLUNA_ESQUERDA,
        template="portlets/_lembretes.html",
        dados=_dados_lembretes,
        ordem=20,
    )
)

registrar(
    Portlet(
        chave="resumo_clientes",
        titulo="Resumo da base de clientes",
        coluna=COLUNA_DIREITA,
        template="portlets/_resumo_clientes.html",
        dados=_dados_resumo_clientes,
        ordem=10,
    )
)

registrar(
    Portlet(
        chave="ultimos_cadastros",
        titulo="Ultimos cadastros",
        coluna=COLUNA_DIREITA,
        template="portlets/_ultimos_cadastros.html",
        dados=_dados_ultimos_cadastros,
        ordem=20,
    )
)
