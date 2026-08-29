from flask import Blueprint, render_template, request
from flask_login import login_required

from app import portlets
from app.models.cliente import Cliente
from app.models.contato import Contato
from app.utils.validators import apenas_digitos

main_bp = Blueprint("main", __name__)

LIMITE_BUSCA = 5
MINIMO_BUSCA = 2


@main_bp.route("/")
@login_required
def index():
    """Painel inicial montado a partir do registro de portlets."""
    return render_template(
        "index.html",
        titulo="Painel",
        coluna_esquerda=portlets.montar(portlets.COLUNA_ESQUERDA),
        coluna_direita=portlets.montar(portlets.COLUNA_DIREITA),
    )


@main_bp.route("/busca")
@login_required
def busca():
    """Busca global do topo: procura em clientes e contatos ao mesmo tempo.

    Responde sempre com um fragmento, consumido pelo HTMX. Abaixo do
    minimo de caracteres devolve vazio, evitando consultar o banco a
    cada tecla digitada.
    """
    termo = (request.args.get("q") or "").strip()

    if len(termo) < MINIMO_BUSCA:
        return render_template(
            "_busca_resultados.html", termo=termo, clientes=[], contatos=[], curto=True
        )

    like = f"%{termo}%"
    digitos = apenas_digitos(termo)

    filtros_cliente = [
        Cliente.nome.ilike(like),
        Cliente.nome_fantasia.ilike(like),
        Cliente.email.ilike(like),
    ]
    if digitos:
        filtros_cliente.append(Cliente.documento.like(f"%{digitos}%"))

    from app import db

    clientes = (
        Cliente.query.filter(db.or_(*filtros_cliente))
        .order_by(Cliente.nome)
        .limit(LIMITE_BUSCA)
        .all()
    )

    contatos = (
        Contato.query.filter(
            db.or_(Contato.nome.ilike(like), Contato.email.ilike(like))
        )
        .order_by(Contato.nome)
        .limit(LIMITE_BUSCA)
        .all()
    )

    return render_template(
        "_busca_resultados.html",
        termo=termo,
        clientes=clientes,
        contatos=contatos,
        curto=False,
    )
