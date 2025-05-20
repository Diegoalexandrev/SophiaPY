from flask import Flask
from .database import db
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    # Configura o banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SECRET_KEY'] = SECRET_KEY  
    db.init_app(app)

    # Importa os modelos
    from .models import Usuario, Livros

    return app
