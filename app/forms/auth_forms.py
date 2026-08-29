from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    email = StringField(
        "E-mail",
        validators=[DataRequired("Informe o e-mail."), Email("E-mail invalido."), Length(max=120)],
    )
    senha = PasswordField("Senha", validators=[DataRequired("Informe a senha.")])
    lembrar = BooleanField("Manter conectado")
    submit = SubmitField("Entrar")
