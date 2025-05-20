from flask import Blueprint, request, redirect, url_for, render_template
from ..utils import verificar_token  

home_bp = Blueprint('home', __name__)  

@home_bp.route('/')
def index():
    token = request.cookies.get('token')
    if not token or not verificar_token(token):
        return redirect(url_for('auth.login'))  # Atualizado para 'auth.login'
    return render_template('index.html')