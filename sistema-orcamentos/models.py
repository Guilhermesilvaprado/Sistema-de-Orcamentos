from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    telefone = db.Column(db.String(20))

    orcamentos = db.relationship("Orcamento", backref="cliente", lazy=True)


class Produto(db.Model):
    __tablename__ = "produtos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255))
    preco_base = db.Column(db.Float, nullable=False, default=0.0)

    orcamentos = db.relationship("Orcamento", backref="produto", lazy=True)


class Orcamento(db.Model):
    __tablename__ = "orcamentos"

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), nullable=False)

    valor_total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="Pendente")
    data_criacao = db.Column(db.DateTime, default=datetime.now)