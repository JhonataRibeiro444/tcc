from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import SubmitField


class ImportarClientesForm(FlaskForm):
    arquivo = FileField(
        "Planilha (.xlsx ou .csv)",
        validators=[
            FileRequired("Selecione um arquivo."),
            FileAllowed(["xlsx", "csv"], "Envie um arquivo .xlsx ou .csv."),
        ],
    )
    submit = SubmitField("Enviar e pre-visualizar")
