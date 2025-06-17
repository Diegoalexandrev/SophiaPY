from main.models import Usuario, CargoEnum

def verificar_login(matricula, senha):
   
    usuario = Usuario.query.filter_by(matricula=matricula).first()

    if not usuario or not usuario.verificar_senha(senha):
        raise ValueError("Usuario ou Senha Invalidos")
    
    if usuario.cargo != CargoEnum.BIBLIOTECARIO:
        raise ValueError("Acesso negado. Apenas bibliotecários podem acessar.")

    return usuario
