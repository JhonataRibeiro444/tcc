from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError

from app.models.cliente import Cliente
from app.utils.validators import apenas_digitos, validar_documento

UFS = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS",
    "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC",
    "SP", "SE", "TO",
]


class ClienteForm(FlaskForm):
    tipo_pessoa = SelectField(
        "Tipo de pessoa",
        choices=[("F", "Pessoa fisica"), ("J", "Pessoa juridica")],
        validators=[DataRequired()],
    )
    nome = StringField(
        "Nome / Razao social",
        validators=[DataRequired("Informe o nome do cliente."), Length(max=150)],
    )
    nome_fantasia = StringField("Nome fantasia", validators=[Optional(), Length(max=150)])
    documento = StringField(
        "CPF / CNPJ", validators=[DataRequired("Informe o CPF ou CNPJ."), Length(max=20)]
    )

    email = StringField(
        "E-mail", validators=[Optional(), Email("E-mail invalido."), Length(max=120)]
    )
    telefone = StringField("Telefone", validators=[Optional(), Length(max=20)])

    cep = StringField("CEP", validators=[Optional(), Length(max=10)])
    logradouro = StringField("Logradouro", validators=[Optional(), Length(max=150)])
    numero = StringField("Numero", validators=[Optional(), Length(max=20)])
    complemento = StringField("Complemento", validators=[Optional(), Length(max=80)])
    bairro = StringField("Bairro", validators=[Optional(), Length(max=80)])
    cidade = StringField("Cidade", validators=[Optional(), Length(max=80)])
    uf = SelectField(
        "UF",
        choices=[("", "--")] + [(uf, uf) for uf in UFS],
        validators=[Optional()],
    )

    observacoes = TextAreaField("Observacoes", validators=[Optional()])
    ativo = BooleanField("Cliente ativo", default=True)
    submit = SubmitField("Salvar")

    def __init__(self, *args, cliente_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Guardado para permitir que o proprio cliente mantenha seu documento
        # ao ser editado, sem cair na verificacao de duplicidade.
        self.cliente_id = cliente_id

    def validate_documento(self, field):
        numeros = apenas_digitos(field.data)

        if not validar_documento(numeros, self.tipo_pessoa.data):
            rotulo = "CPF" if self.tipo_pessoa.data == "F" else "CNPJ"
            raise ValidationError(f"{rotulo} invalido.")

        existente = Cliente.query.filter_by(documento=numeros).first()
        if existente and existente.id != self.cliente_id:
            raise ValidationError("Ja existe um cliente cadastrado com este documento.")
