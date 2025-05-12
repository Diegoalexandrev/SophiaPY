from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração da conexão com o PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/projetoIntegrador'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo (tabela) no banco de dados
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Cria as tabelas no banco de dados (se ainda não existirem)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return 'Servidor Flask rodando!'

@app.route('/inserir')
def inserir_usuario():
    novo_usuario = Usuario(nome='João Silva', email='joao@example.com')
    db.session.add(novo_usuario)
    db.session.commit()
    return 'Usuário inserido com sucesso!'

@app.route('/usuarios')
def listar_usuarios():
    usuarios = Usuario.query.all()
    resultado = ''
    for u in usuarios:
        resultado += f'ID: {u.id} | Nome: {u.nome} | Email: {u.email}<br>'
    return resultado


if __name__ == '__main__':
    app.run(debug=True)
