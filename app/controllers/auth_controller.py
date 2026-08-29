from urllib.parse import urlparse

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.forms.auth_forms import LoginForm
from app.models.usuario import Usuario

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def _destino_seguro(destino):
    """Evita redirecionamento para dominios externos apos o login."""
    if not destino:
        return None
    partes = urlparse(destino)
    if partes.netloc or partes.scheme:
        return None
    return destino


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()

    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data.lower().strip()).first()

        if usuario is None or not usuario.verificar_senha(form.senha.data):
            # Mensagem generica: nao revela se o e-mail existe na base.
            flash("E-mail ou senha incorretos.", "danger")
        elif not usuario.ativo:
            flash("Este usuario esta desativado.", "warning")
        else:
            login_user(usuario, remember=form.lembrar.data)
            destino = _destino_seguro(request.args.get("next"))
            return redirect(destino or url_for("main.index"))

    return render_template("auth/login.html", form=form, titulo="Entrar")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sessao encerrada.", "info")
    return redirect(url_for("auth.login"))
