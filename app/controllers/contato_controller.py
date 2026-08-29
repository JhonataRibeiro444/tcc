from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required

from app import db
from app.forms.contato_forms import ContatoForm
from app.models.cliente import Cliente
from app.models.contato import Contato
from app.utils.validators import apenas_digitos

contato_bp = Blueprint("contatos", __name__)


def _e_requisicao_htmx():
    return request.headers.get("HX-Request") == "true"


def _painel(cliente, form=None, contato_em_edicao=None, mostrar_form=False):
    """Renderiza o painel de contatos, usado como resposta parcial do HTMX."""
    return render_template(
        "contatos/_painel.html",
        cliente=cliente,
        form_contato=form or ContatoForm(),
        contato_em_edicao=contato_em_edicao,
        mostrar_form=mostrar_form,
    )


def _resposta(cliente, **kwargs):
    if _e_requisicao_htmx():
        return _painel(cliente, **kwargs)
    return redirect(url_for("clientes.detalhar", cliente_id=cliente.id))


def _definir_principal(cliente, contato):
    """Garante que exista no maximo um contato principal por cliente."""
    for outro in cliente.contatos:
        if outro is not contato:
            outro.principal = False


def _aplicar_form_no_contato(form, contato):
    contato.nome = form.nome.data.strip()
    contato.cargo = (form.cargo.data or "").strip() or None
    contato.email = (form.email.data or "").strip().lower() or None
    contato.telefone = apenas_digitos(form.telefone.data) or None
    contato.observacoes = (form.observacoes.data or "").strip() or None
    contato.principal = form.principal.data


@contato_bp.route("/contatos")
@login_required
def listar():
    """Listagem geral de contatos, com busca por nome, e-mail ou cliente."""
    busca = (request.args.get("busca") or "").strip()
    pagina = request.args.get("pagina", 1, type=int)

    consulta = Contato.query.join(Cliente)

    if busca:
        termo = f"%{busca}%"
        consulta = consulta.filter(
            db.or_(
                Contato.nome.ilike(termo),
                Contato.email.ilike(termo),
                Contato.cargo.ilike(termo),
                Cliente.nome.ilike(termo),
            )
        )

    paginacao = consulta.order_by(Contato.nome).paginate(
        page=pagina,
        per_page=current_app.config["ITENS_POR_PAGINA"],
        error_out=False,
    )

    contexto = {
        "paginacao": paginacao,
        "contatos": paginacao.items,
        "busca": busca,
        "titulo": "Contatos",
    }

    if _e_requisicao_htmx():
        return render_template("contatos/_tabela.html", **contexto)

    return render_template("contatos/lista.html", **contexto)


@contato_bp.route("/clientes/<int:cliente_id>/contatos/novo")
@login_required
def novo(cliente_id):
    cliente = db.get_or_404(Cliente, cliente_id)
    return _resposta(cliente, form=ContatoForm(), mostrar_form=True)


@contato_bp.route("/clientes/<int:cliente_id>/contatos/cancelar")
@login_required
def cancelar(cliente_id):
    cliente = db.get_or_404(Cliente, cliente_id)
    return _resposta(cliente)


@contato_bp.route("/clientes/<int:cliente_id>/contatos", methods=["POST"])
@login_required
def criar(cliente_id):
    cliente = db.get_or_404(Cliente, cliente_id)
    form = ContatoForm()

    if not form.validate_on_submit():
        return _resposta(cliente, form=form, mostrar_form=True)

    contato = Contato(cliente_id=cliente.id)
    _aplicar_form_no_contato(form, contato)
    db.session.add(contato)

    if contato.principal:
        _definir_principal(cliente, contato)

    db.session.commit()
    flash("Contato adicionado.", "success")
    return _resposta(cliente)


@contato_bp.route("/contatos/<int:contato_id>/editar", methods=["GET", "POST"])
@login_required
def editar(contato_id):
    contato = db.get_or_404(Contato, contato_id)
    cliente = contato.cliente

    if request.method == "GET":
        form = ContatoForm(obj=contato)
        form.telefone.data = contato.telefone_formatado
        return _resposta(cliente, form=form, contato_em_edicao=contato, mostrar_form=True)

    form = ContatoForm()
    if not form.validate_on_submit():
        return _resposta(cliente, form=form, contato_em_edicao=contato, mostrar_form=True)

    _aplicar_form_no_contato(form, contato)
    if contato.principal:
        _definir_principal(cliente, contato)

    db.session.commit()
    flash("Contato atualizado.", "success")
    return _resposta(cliente)


@contato_bp.route("/contatos/<int:contato_id>/excluir", methods=["POST"])
@login_required
def excluir(contato_id):
    contato = db.get_or_404(Contato, contato_id)
    cliente = contato.cliente

    db.session.delete(contato)
    db.session.commit()
    flash("Contato removido.", "info")
    return _resposta(cliente)
