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
from app.forms.cliente_forms import ClienteForm
from app.models.cliente import Cliente
from app.utils.validators import apenas_digitos

cliente_bp = Blueprint("clientes", __name__, url_prefix="/clientes")

# Recortes usados pelos portlets do painel para apontar direto para uma
# lista ja filtrada.
ROTULOS_FILTRO = {
    "sem_contato": "clientes ativos sem contato cadastrado",
    "incompleto": "clientes sem e-mail ou telefone",
}

ROTULOS_TIPO = {
    "F": "somente pessoas fisicas",
    "J": "somente pessoas juridicas",
}


def _e_requisicao_htmx():
    return request.headers.get("HX-Request") == "true"


def _aplicar_form_no_cliente(form, cliente):
    """Copia os dados do formulario para o model, normalizando os campos."""
    cliente.tipo_pessoa = form.tipo_pessoa.data
    cliente.nome = form.nome.data.strip()
    cliente.nome_fantasia = (form.nome_fantasia.data or "").strip() or None
    cliente.documento = apenas_digitos(form.documento.data)
    cliente.email = (form.email.data or "").strip().lower() or None
    cliente.telefone = apenas_digitos(form.telefone.data) or None
    cliente.cep = apenas_digitos(form.cep.data) or None
    cliente.logradouro = (form.logradouro.data or "").strip() or None
    cliente.numero = (form.numero.data or "").strip() or None
    cliente.complemento = (form.complemento.data or "").strip() or None
    cliente.bairro = (form.bairro.data or "").strip() or None
    cliente.cidade = (form.cidade.data or "").strip() or None
    cliente.uf = form.uf.data or None
    cliente.observacoes = (form.observacoes.data or "").strip() or None
    cliente.ativo = form.ativo.data


@cliente_bp.route("/")
@login_required
def listar():
    """Listagem com busca livre e filtros auxiliares.

    Quando a requisicao vem do HTMX devolve apenas a tabela, o que permite
    atualizar o resultado da busca sem recarregar a pagina inteira.

    Os filtros `filtro` e `tipo` existem para que os portlets do painel
    consigam apontar direto para um recorte da base.
    """
    busca = (request.args.get("busca") or "").strip()
    situacao = request.args.get("situacao") or "todos"
    filtro = request.args.get("filtro") or ""
    tipo = request.args.get("tipo") or ""
    pagina = request.args.get("pagina", 1, type=int)

    consulta = Cliente.query

    if busca:
        termo = f"%{busca}%"
        digitos = apenas_digitos(busca)
        condicoes = [
            Cliente.nome.ilike(termo),
            Cliente.nome_fantasia.ilike(termo),
            Cliente.email.ilike(termo),
        ]
        if digitos:
            condicoes.append(Cliente.documento.like(f"%{digitos}%"))
        consulta = consulta.filter(db.or_(*condicoes))

    if situacao == "ativos":
        consulta = consulta.filter_by(ativo=True)
    elif situacao == "inativos":
        consulta = consulta.filter_by(ativo=False)

    if tipo in ("F", "J"):
        consulta = consulta.filter_by(tipo_pessoa=tipo)

    if filtro == "sem_contato":
        consulta = consulta.filter(~Cliente.contatos.any(), Cliente.ativo.is_(True))
    elif filtro == "incompleto":
        consulta = consulta.filter(
            Cliente.ativo.is_(True),
            db.or_(Cliente.email.is_(None), Cliente.telefone.is_(None)),
        )

    paginacao = consulta.order_by(Cliente.nome).paginate(
        page=pagina,
        per_page=current_app.config["ITENS_POR_PAGINA"],
        error_out=False,
    )

    contexto = {
        "paginacao": paginacao,
        "clientes": paginacao.items,
        "busca": busca,
        "situacao": situacao,
        "filtro": filtro,
        "tipo": tipo,
        "rotulo_filtro": ROTULOS_FILTRO.get(filtro) or ROTULOS_TIPO.get(tipo),
        "titulo": "Clientes",
    }

    if _e_requisicao_htmx():
        return render_template("clientes/_tabela.html", **contexto)

    return render_template("clientes/lista.html", **contexto)


@cliente_bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo():
    form = ClienteForm()

    if form.validate_on_submit():
        cliente = Cliente()
        _aplicar_form_no_cliente(form, cliente)
        db.session.add(cliente)
        db.session.commit()
        flash("Cliente cadastrado com sucesso.", "success")
        return redirect(url_for("clientes.detalhar", cliente_id=cliente.id))

    return render_template(
        "clientes/form.html", form=form, cliente=None, titulo="Novo cliente"
    )


@cliente_bp.route("/<int:cliente_id>")
@login_required
def detalhar(cliente_id):
    from app.forms.contato_forms import ContatoForm

    cliente = db.get_or_404(Cliente, cliente_id)
    return render_template(
        "clientes/detalhe.html",
        cliente=cliente,
        form_contato=ContatoForm(),
        contato_em_edicao=None,
        mostrar_form=False,
        titulo=cliente.nome,
    )


@cliente_bp.route("/<int:cliente_id>/editar", methods=["GET", "POST"])
@login_required
def editar(cliente_id):
    cliente = db.get_or_404(Cliente, cliente_id)
    form = ClienteForm(obj=cliente, cliente_id=cliente.id)

    if request.method == "GET":
        # Mostra o documento com mascara na tela de edicao.
        form.documento.data = cliente.documento_formatado
        form.telefone.data = cliente.telefone_formatado

    if form.validate_on_submit():
        _aplicar_form_no_cliente(form, cliente)
        db.session.commit()
        flash("Cliente atualizado.", "success")
        return redirect(url_for("clientes.detalhar", cliente_id=cliente.id))

    return render_template(
        "clientes/form.html",
        form=form,
        cliente=cliente,
        titulo=f"Editar {cliente.nome}",
    )


@cliente_bp.route("/<int:cliente_id>/situacao", methods=["POST"])
@login_required
def alternar_situacao(cliente_id):
    """Ativa ou inativa o cliente em vez de apaga-lo, preservando o historico."""
    cliente = db.get_or_404(Cliente, cliente_id)
    cliente.ativo = not cliente.ativo
    db.session.commit()

    estado = "reativado" if cliente.ativo else "inativado"
    flash(f"Cliente {estado}.", "success")
    return redirect(url_for("clientes.detalhar", cliente_id=cliente.id))
