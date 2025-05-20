from flask import Blueprint, request, jsonify
from ..schemas import LoginSchema
from ..services import verificar_login
from .. import auth_bp

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        dados = LoginSchema().load(request.json)
        usuario = verificar_login(dados['matricula'], dados['senha'])
        return jsonify({"token": usuario.gerar_token()})
    except ValueError as e:
        return jsonify({"erro": str(e)}), 401
    except Exception as e:
        return jsonify({"erro": "Erro inesperado"}), 500
