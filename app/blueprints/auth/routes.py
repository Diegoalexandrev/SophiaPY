from .schemas import LoginSchema
from .services import verificar_login

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    dados = LoginSchema().load(request.json)
    usuario = verificar_login(dados['email'], dados['senha'])
    return jsonify({"token": usuario.gerar_token()})