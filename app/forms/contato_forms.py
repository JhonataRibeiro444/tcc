from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional


class ContatoForm(FlaskForm):
    nome = StringField(
        "Nome", validators=[DataRequired("Informe o nome do contato."), Length(max=150)]
    )
    cargo = StringField("Cargo", validators=[Optional(), Length(max=80)])
    email = StringField(
        "E-mail", validators=[Optional(), Email("E-mail invalido."), Length(max=120)]
    )
    telefone = StringField("Telefone", validators=[Optional(), Length(max=20)])
    principal = BooleanField("Contato principal")
    observacoes = TextAreaField("Observacoes", validators=[Optional()])
    submit = SubmitField("Salvar contato")
