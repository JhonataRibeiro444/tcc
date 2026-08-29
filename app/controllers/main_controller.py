from flask import Blueprint, render_template
from flask_login import login_required

from app.models.cliente import Cliente
from app.models.contato import Contato

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def index():
    """Painel inicial com os indicadores basicos da base de clientes."""
    total_clientes = Cliente.query.count()
    clientes_ativos = Cliente.query.filter_by(ativo=True).count()
    total_contatos = Contato.query.count()

    ultimos_clientes = (
        Cliente.query.order_by(Cliente.criado_em.desc()).limit(5).all()
    )

    return render_template(
        "index.html",
        titulo="Painel",
        total_clientes=total_clientes,
        clientes_ativos=clientes_ativos,
        clientes_inativos=total_clientes - clientes_ativos,
        total_contatos=total_contatos,
        ultimos_clientes=ultimos_clientes,
    )
