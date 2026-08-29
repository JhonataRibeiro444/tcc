from datetime import datetime, timezone

from app import db
from app.utils.validators import formatar_documento, formatar_telefone

TIPOS_PESSOA = {"F": "Pessoa fisica", "J": "Pessoa juridica"}


class Cliente(db.Model):
    """Cliente do CRM, pessoa fisica ou juridica."""

    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)

    tipo_pessoa = db.Column(db.String(1), nullable=False, default="F")
    nome = db.Column(db.String(150), nullable=False, index=True)
    nome_fantasia = db.Column(db.String(150))
    documento = db.Column(db.String(14), nullable=False, unique=True, index=True)

    email = db.Column(db.String(120))
    telefone = db.Column(db.String(11))

    cep = db.Column(db.String(8))
    logradouro = db.Column(db.String(150))
    numero = db.Column(db.String(20))
    complemento = db.Column(db.String(80))
    bairro = db.Column(db.String(80))
    cidade = db.Column(db.String(80))
    uf = db.Column(db.String(2))

    observacoes = db.Column(db.Text)
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    criado_em = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    atualizado_em = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    contatos = db.relationship(
        "Contato",
        back_populates="cliente",
        cascade="all, delete-orphan",
        order_by="Contato.nome",
    )

    @property
    def tipo_pessoa_label(self):
        return TIPOS_PESSOA.get(self.tipo_pessoa, "")

    @property
    def documento_formatado(self):
        return formatar_documento(self.documento)

    @property
    def telefone_formatado(self):
        return formatar_telefone(self.telefone)

    @property
    def contato_principal(self):
        for contato in self.contatos:
            if contato.principal:
                return contato
        return None

    @property
    def endereco_resumido(self):
        partes = [p for p in (self.cidade, self.uf) if p]
        return " - ".join(partes)

    def __repr__(self):
        return f"<Cliente {self.nome}>"
