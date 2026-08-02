from app import db


class Example(db.Model):
    __tablename__ = "examples"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<Example {self.nome}>"
