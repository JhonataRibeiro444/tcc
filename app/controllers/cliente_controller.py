from datetime import datetime, timezone

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
from flask_login import login_required
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.forms.cliente_forms import ClienteForm
from app.forms.planilha_forms import ImportarClientesForm
from app.models.cliente import Cliente
from app.models.contato import Contato
from app.utils import planilhas
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


def _consulta_clientes_filtrada(busca, situacao, filtro, tipo):
    """Monta a consulta de clientes a partir dos mesmos filtros usados na
    listagem. Compartilhada com a exportacao, para que o arquivo exportado
    respeite exatamente o recorte que esta sendo visto na tela."""
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

    return consulta


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

    consulta = _consulta_clientes_filtrada(busca, situacao, filtro, tipo)

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


@cliente_bp.route("/exportar")
@login_required
def exportar():
    """Exporta para .xlsx ou .csv os clientes que estao sendo vistos na
    listagem, respeitando os mesmos filtros (busca, situacao, tipo, recorte)."""
    formato = request.args.get("formato", "xlsx")
    busca = (request.args.get("busca") or "").strip()
    situacao = request.args.get("situacao") or "todos"
    filtro = request.args.get("filtro") or ""
    tipo = request.args.get("tipo") or ""

    clientes = (
        _consulta_clientes_filtrada(busca, situacao, filtro, tipo)
        .order_by(Cliente.nome)
        .all()
    )

    agora = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M")

    if formato == "csv":
        return send_file(
            planilhas.exportar_clientes_csv(clientes),
            mimetype="text/csv",
            as_attachment=True,
            download_name=f"clientes-{agora}.csv",
        )

    return send_file(
        planilhas.exportar_clientes_xlsx(clientes),
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name=f"clientes-{agora}.xlsx",
    )


@cliente_bp.route("/importar/modelo")
@login_required
def importar_modelo():
    """Planilha .xlsx de exemplo, com os cabecalhos que a importacao espera."""
    return send_file(
        planilhas.gerar_modelo_importacao(),
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name="modelo-importacao-clientes.xlsx",
    )


@cliente_bp.route("/importar", methods=["GET", "POST"])
@login_required
def importar():
    """Recebe a planilha, valida linha a linha e encaminha para a
    pre-visualizacao. Nada e gravado no banco nesta etapa."""
    form = ImportarClientesForm()

    if form.validate_on_submit():
        arquivo = form.arquivo.data
        try:
            linhas = planilhas.ler_planilha(arquivo.stream, arquivo.filename)
        except ValueError as erro:
            flash(str(erro), "danger")
            return render_template(
                "clientes/importar.html", form=form, titulo="Importar clientes"
            )

        if not linhas:
            flash("A planilha nao tem nenhuma linha para importar.", "warning")
            return render_template(
                "clientes/importar.html", form=form, titulo="Importar clientes"
            )

        processadas = planilhas.validar_linhas(linhas)
        token = planilhas.salvar_pendente(processadas, arquivo.filename)
        return redirect(url_for("clientes.importar_preview", token=token))

    return render_template("clientes/importar.html", form=form, titulo="Importar clientes")


@cliente_bp.route("/importar/<token>")
@login_required
def importar_preview(token):
    """Mostra o resultado da validacao antes de gravar qualquer coisa."""
    pendente = planilhas.carregar_pendente(token)
    if pendente is None:
        flash(
            "Essa importacao expirou ou ja foi processada. Envie a planilha novamente.",
            "warning",
        )
        return redirect(url_for("clientes.importar"))

    ok, duplicados, erros = planilhas.linhas_por_status(pendente)
    return render_template(
        "clientes/importar_preview.html",
        titulo="Conferir importacao",
        token=token,
        arquivo=pendente["arquivo"],
        linhas=pendente["linhas"],
        total_ok=len(ok),
        total_duplicados=len(duplicados),
        total_erros=len(erros),
    )


@cliente_bp.route("/importar/<token>/erros")
@login_required
def importar_erros(token):
    """CSV com as linhas nao importadas (duplicadas ou com erro) e o motivo."""
    pendente = planilhas.carregar_pendente(token)
    if pendente is None:
        flash("Essa importacao expirou ou ja foi processada.", "warning")
        return redirect(url_for("clientes.importar"))

    return send_file(
        planilhas.gerar_relatorio_erros(pendente),
        mimetype="text/csv",
        as_attachment=True,
        download_name="linhas-nao-importadas.csv",
    )


@cliente_bp.route("/importar/<token>/confirmar", methods=["POST"])
@login_required
def importar_confirmar(token):
    """Grava as linhas validadas como "ok". Cada cliente entra em sua propria
    transacao, para que um problema numa linha nao derrube as demais."""
    pendente = planilhas.carregar_pendente(token)
    if pendente is None:
        flash(
            "Essa importacao expirou ou ja foi processada. Envie a planilha novamente.",
            "warning",
        )
        return redirect(url_for("clientes.importar"))

    ok, duplicados, erros = planilhas.linhas_por_status(pendente)

    importados = 0
    for linha in ok:
        dados = linha["dados"]

        # Entre a pre-visualizacao e a confirmacao outro cadastro pode ter
        # usado o mesmo documento; revalida aqui em vez de confiar so no
        # status calculado na etapa anterior.
        if Cliente.query.filter_by(documento=dados["documento"]).first():
            continue

        try:
            cliente = Cliente(
                tipo_pessoa=dados["tipo_pessoa"],
                nome=dados["nome"],
                nome_fantasia=dados["nome_fantasia"] or None,
                documento=dados["documento"],
                email=dados["email"] or None,
                telefone=dados["telefone"] or None,
                cep=dados["cep"] or None,
                logradouro=dados["logradouro"] or None,
                numero=dados["numero"] or None,
                complemento=dados["complemento"] or None,
                bairro=dados["bairro"] or None,
                cidade=dados["cidade"] or None,
                uf=dados["uf"] or None,
                observacoes=dados["observacoes"] or None,
                ativo=True,
            )
            db.session.add(cliente)

            if dados["contato_nome"]:
                db.session.flush()  # garante cliente.id antes de criar o contato
                db.session.add(
                    Contato(
                        cliente_id=cliente.id,
                        nome=dados["contato_nome"],
                        cargo=dados["contato_cargo"] or None,
                        email=dados["contato_email"] or None,
                        telefone=dados["contato_telefone"] or None,
                        principal=True,
                    )
                )

            db.session.commit()
            importados += 1
        except SQLAlchemyError:
            db.session.rollback()

    planilhas.descartar_pendente(token)

    flash(
        f"{importados} cliente(s) importado(s). "
        f"{len(duplicados)} ja cadastrado(s) (nao importado(s)). "
        f"{len(erros)} com erro (nao importado(s)).",
        "success" if importados else "warning",
    )
    return redirect(url_for("clientes.listar"))
