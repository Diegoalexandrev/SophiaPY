from flask_sqlalchemy import SQLAlchemy
from .database import db
from enum import Enum
from datetime import date

class CargoEnum(Enum):
    BIBLIOTECARIO = 'Bibliotecario'
    ASSISTENTE = 'Assistente'

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

    emprestimos = db.relationship('Emprestimos', back_populates='usuario')
    reservas = db.relationship('Reservas', back_populates='usuario')


class Livros(db.Model):
    __tablename__ = 'livros'  
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    ano_publicacao = db.Column(db.Date, nullable=False)
    categoria = db.Column(db.String(120))
    isbn = db.Column(db.String(100), nullable=False) 
    capa = db.Column(db.LargeBinary)
    curso = db.Column(db.String(100), nullable=False)  

    autores = db.relationship("Autores", secondary="livros_autores", back_populates="livros")
    exemplares = db.relationship('Exemplares', back_populates='livro')
    emprestimos = db.relationship('Emprestimos', back_populates='livro')

class Autores(db.Model):
    __tablename__ = 'autores'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)

    livros = db.relationship("Livros", secondary="livros_autores", back_populates="autores")

livros_autores = db.Table(
    'livros_autores',
    db.Column('livro_id', db.Integer, db.ForeignKey('livros.id'), primary_key=True),
    db.Column('autor_id', db.Integer, db.ForeignKey('autores.id'), primary_key=True)
)

class Emprestimos(db.Model):
    __tablename__ = 'emprestimos'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    livro_id = db.Column(db.Integer, db.ForeignKey('livros.id'), nullable=False)
    data_emprestimo = db.Column(db.Date, nullable=False, default=date.today)
    data_devolucao = db.Column(db.Date)
    devolvido = db.Column(db.Boolean, default=False)

    usuario = db.relationship('Usuario', back_populates='emprestimos')
    livro = db.relationship('Livros', back_populates='emprestimos')

class EstadoExemplar(Enum):
    DISPONIVEL = 'Disponível'
    EMPRESTADO = 'Emprestado'
    RESERVADO = 'Reservado'
    MANUTENCAO = 'Em Manutenção'

class Exemplares(db.Model):
    __tablename__ = 'exemplares'
    id = db.Column(db.Integer, primary_key=True)
    livro_id = db.Column(db.Integer, db.ForeignKey('livros.id'), nullable=False)
    numero_chamada = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.Enum(EstadoExemplar), nullable=False, default=EstadoExemplar.DISPONIVEL)

    livro = db.relationship('Livros', back_populates='exemplares')
    reservas = db.relationship('Reservas', back_populates='exemplar')

class StatusReserva(Enum):
    ATIVA = 'Ativa'
    CANCELADA = 'Cancelada'
    CONCLUIDA = 'Concluída'

class Reservas(db.Model):
    __tablename__ = 'reservas'
    id = db.Column(db.Integer, primary_key=True)
    exemplar_id = db.Column(db.Integer, db.ForeignKey('exemplares.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    data_reserva = db.Column(db.Date, nullable=False, default=date.today)
    status = db.Column(db.Enum(StatusReserva), nullable=False, default=StatusReserva.ATIVA)
    
    exemplar = db.relationship('Exemplares', back_populates='reservas')
    usuario = db.relationship('Usuario', back_populates='reservas')