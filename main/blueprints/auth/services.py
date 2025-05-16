from main.models import Usuario

def verificar_login(email, senha):
    # Tenta buscar o usuário pelo email
    usuario = Usuario.query.filter_by(email=email).first()

    # Se o usuário não for encontrado ou a senha não for válida
    if not usuario or not usuario.verificar_senha(senha):
        raise ValueError("Credenciais inválidas")

    # Retorna o usuário se tudo estiver certo
    return usuario
