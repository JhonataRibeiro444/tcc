"""Comandos de linha de comando para preparar o ambiente local."""

import click

from app import db


def registrar_comandos(app):
    @app.cli.command("init-db")
    def init_db():
        """Cria as tabelas do banco de dados."""
        from app.models import Cliente, Contato, Usuario  # noqa: F401

        db.create_all()
        click.echo("Tabelas criadas.")

    @app.cli.command("criar-usuario")
    @click.argument("nome")
    @click.argument("email")
    @click.argument("senha")
    def criar_usuario(nome, email, senha):
        """Cria um usuario para acessar o sistema."""
        from app.models.usuario import Usuario

        db.create_all()
        if Usuario.query.filter_by(email=email.lower()).first():
            click.echo("Ja existe um usuario com esse e-mail.")
            return

        usuario = Usuario(nome=nome, email=email.lower())
        usuario.definir_senha(senha)
        db.session.add(usuario)
        db.session.commit()
        click.echo(f"Usuario {email.lower()} criado.")
