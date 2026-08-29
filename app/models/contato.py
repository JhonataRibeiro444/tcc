from datetime import datetime, timezone

from app import db
from app.utils.validators import formatar_telefone


class Contato(db.Model):
    """Pessoa de contato vinculada a um cliente."""

    __tablename__ = "contatos"

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    nome = db.Column(db.String(150), nullable=False)
    cargo = db.Column(db.String(80))
    email = db.Column(db.String(120))
    telefone = db.Column(db.String(11))
    principal = db.Column(db.Boolean, nullable=False, default=False)
    observacoes = db.Column(db.Text)

    criado_em = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    cliente = db.relationship("Cliente", back_populates="contatos")

    @property
    def telefone_formatado(self):
        return formatar_telefone(self.telefone)

    def __repr__(self):
        return f"<Contato {self.nome}>"
