def verificar_login(email, senha):
    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario or not usuario.verificar_senha(senha):
        raise ValueError("Credenciais inválidas")
    return usuario