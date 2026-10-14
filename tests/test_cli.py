from sqlalchemy import inspect

from app import db
from app.models.usuario import Usuario


def test_init_db_cria_as_tabelas(app):
    db.drop_all()

    resultado = app.test_cli_runner().invoke(args=["init-db"])

    assert "Tabelas criadas." in resultado.output
    tabelas = inspect(db.engine).get_table_names()
    assert {"usuarios", "clientes", "contatos"} <= set(tabelas)


def test_criar_usuario_grava_senha_em_hash(app):
    resultado = app.test_cli_runner().invoke(
        args=["criar-usuario", "Ana", "Ana@Exemplo.com", "senha-forte"]
    )

    assert "Usuario ana@exemplo.com criado." in resultado.output
    usuario = Usuario.query.filter_by(email="ana@exemplo.com").one()
    assert usuario.senha_hash != "senha-forte"
    assert usuario.verificar_senha("senha-forte")


def test_criar_usuario_recusa_email_repetido(app):
    resultado = app.test_cli_runner().invoke(
        args=["criar-usuario", "Outro", "teste@exemplo.com", "qualquer"]
    )

    assert "Ja existe um usuario com esse e-mail." in resultado.output
    assert Usuario.query.filter_by(email="teste@exemplo.com").count() == 1
