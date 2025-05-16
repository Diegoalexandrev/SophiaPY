from main import create_app, db  
from main.models import *
from datetime import date, timedelta

# Cria a aplicação a partir da função create_app
app = create_app()

# Usa o contexto da aplicação para acessar o banco
with app.app_context():
    # Cria as tabelas (se ainda não existirem)
    #db.drop_all()
    db.create_all()

    # --- Criar Usuarios ---
    usuario1 = Usuario(
        nome="Joao Silva",
        senha="123456",
        cpf="123.456.789-00",
        email="joao@email.com",
        telefone="(11) 99999-9999",
        data_nascimento=date(1990, 5, 15),
        cargo=CargoEnum.BIBLIOTECARIO,
        matricula=20250001
    )
    usuario2 = Usuario(
        nome="Maria Souza",
        senha="654321",
        cpf="987.654.321-00",
        email="maria@email.com",
        telefone="(11) 98888-8888",
        data_nascimento=date(1985, 10, 20),
        cargo=CargoEnum.ASSISTENTE,
        matricula=20250002
    )
    db.session.add(usuario1)
    db.session.add(usuario2)
    
    db.session.commit()

    print("Usuários adicionados com sucesso:", usuario1.nome, "e", usuario2.nome)

    # --- Criar Autores ---
    autor1 = Autores(nome="Machado de Assis")
    autor2 = Autores(nome="Clarice Lispector")
    autor3 = Autores(nome="J.K. Rowling")

    db.session.add_all([autor1, autor2, autor3])
    db.session.commit()

    print("Autores adicionados com sucesso:", autor1.nome, "e", autor2.nome, "e", autor3.nome)

     # --- Criar Livros ---
    livro1 = Livros(
        titulo="Dom Casmurro",
        ano_publicacao=date(1899, 1, 1),
        categoria="Literatura Brasileira",
        isbn="978-85-1234-567-8",
        curso="Letras"
    )
    livro2 = Livros(
        titulo="Harry Potter e a Pedra Filosofal",
        ano_publicacao=date(1997, 6, 26),
        categoria="Fantasia",
        isbn="978-85-1234-568-5",
        curso="Literatura Estrangeira"
    )
    db.session.add_all([livro1, livro2])
    db.session.commit()

    print("livros adicionados com sucesso:", livro1.titulo, "e", livro2.titulo)

    # --- Criar Livro_Autor ---
    livro1.autores.append(autor1) 
    livro2.autores.append(autor3)  
    db.session.commit()

    # --- Criar Exemplares ---
    exemplar1 = Exemplares(
        livro=livro1,
        numero_chamada="LC869.M33 D6 1899",
        estado=EstadoExemplar.DISPONIVEL
    )
    exemplar2 = Exemplares(
        livro=livro2,
        numero_chamada="PR6068.O93 H37 1997",
        estado=EstadoExemplar.DISPONIVEL
    )
    db.session.add_all([exemplar1, exemplar2])
    db.session.commit()

    # --- Criar Empréstimos ---
    emprestimo1 = Emprestimos(
        usuario=usuario1,
        livro=livro1,
        data_emprestimo=date.today() - timedelta(days=10),
        data_devolucao=date.today() + timedelta(days=7),
        devolvido=False
    )
    emprestimo2 = Emprestimos(
        usuario=usuario2,
        livro=livro2,
        data_emprestimo=date.today() - timedelta(days=5),
        data_devolucao=date.today() + timedelta(days=14),
        devolvido=False
    )

    db.session.add_all([emprestimo1, emprestimo2])
    db.session.commit()

    # --- Criar Reservas ---
    reserva1 = Reservas(
        exemplar=exemplar1,
        usuario=usuario2,
        data_reserva=date.today(),
        status=StatusReserva.ATIVA
    )
    db.session.add(reserva1)
    db.session.commit()

    
