from flask_sqlalchemy import SQLAlchemy
from .database import db
from enum import Enum


class CargoEnum(Enum):
    BIBLIOTECARIO = 'Bibliotecario'
    ASSISTENTE =  'Assistente'

class Usuario(db.Model):
    __tablename__ = 'usuarios'  

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(120), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)

    cargo = db.Column(db.Enum(CargoEnum), nullable=False, default=CargoEnum.ASSISTENTE)
    matricula = db.Column(
        db.Integer,
        db.Sequence('aluno_matricula_seq', start=20250001, increment=1),
        unique=True, 
        nullable=False
    )


class Livros(db.Model):
    __tablename__ = 'livros'  
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    ano_publicacao = db.Column(db.Date, nullable=False)
    categoria = db.Column(db.String(120))
    isbn = db.Column(db.String(100), nullable=False)  # Corrigido aqui
    # Não use para imagens > 1MB (sobrecarrega o banco)
    # Converta para base64 se precisar enviar via JSON:
    capa = db.Column(db.LargeBinary)
    curso = db.Column(db.String(100), nullable=False)  # Corrigido aqui
    



    