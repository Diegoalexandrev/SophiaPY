from flask import Blueprint, request, jsonify
from . import db
from .models import Usuario  

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return jsonify({"status": "Servidor Flask rodando!"})

@bp.route('/usuarios', methods=['POST'])
def criar_usuario():
    try:
        # 1. Recebe dados do frontend/Postman
        dados = request.json
        
        # 2. Validação básica
        if not dados or 'nome' not in dados or 'email' not in dados:
            return jsonify({"erro": "Dados incompletos"}), 400
        
        # 3. Cria usuário
        novo_usuario = Usuario(
            nome=dados['nome'],
            email=dados['email']
            # Adicione outros campos conforme seu modelo
        )
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        return jsonify({
            "mensagem": "Usuário criado com sucesso!",
            "id": novo_usuario.id
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 500