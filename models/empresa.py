from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Empresa(db.Model):
    __tablename__ = 'empresas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cnpj = db.Column(db.String(18), nullable=False)
    nome_razao = db.Column(db.String(255), nullable=False)
    nome_fantasia = db.Column(db.String(255), nullable=True)
    cnae = db.Column(db.String(10), nullable=True)
