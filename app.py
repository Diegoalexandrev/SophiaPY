from main import create_app, db
from main.models import *
from datetime import date, timedelta
from flask import Flask, render_template
import os 
from flask import request
from main.blueprints.home.utils import verificar_token
from main.blueprints.home.routes.home_api import home_bp
from flask import redirect, url_for
from main.blueprints.auth import auth_bp

app = create_app()

# Registra o blueprint
app.register_blueprint(auth_bp)  
app.register_blueprint(home_bp)


# Cria e verifica tabelas
with app.app_context():
    print("↓ Verificando tabelas existentes...")
    inspector = db.inspect(db.engine)
    print("Tabelas antes:", inspector.get_table_names())

    db.drop_all()
    db.create_all()

    if not Usuario.query.first():
        print("Populando dados iniciais...")

            # --- Criar Usuarios ---
        usuario1 = Usuario(
            nome="Joao Silva",
            cpf="123.456.789-00",
            email="joao@email.com",
            telefone="(11) 99999-9999",
            data_nascimento=date(1990, 5, 15),
            cargo=CargoEnum.BIBLIOTECARIO,
            matricula=20250001,
        )
        usuario1.set_senha("123456")
        usuario2 = Usuario(
            nome="Maria Souza",
            cpf="987.654.321-00",
            email="maria@email.com",
            telefone="(11) 98888-8888",
            data_nascimento=date(1985, 10, 20),
            cargo=CargoEnum.ASSISTENTE,
            matricula=20250002
        )
        usuario3 = Usuario(
            nome="Carlos Pereira",
            cpf="111.222.333-44",
            email="carlos@email.com",
            telefone="(11) 97777-7777",
            data_nascimento=date(2000, 3, 10),
            cargo=CargoEnum.ALUNO,
            matricula=20250003
        )
        usuario3.set_senha("123456")       
        usuario1.set_senha("123456")
        usuario2.set_senha("123456")
        db.session.add(usuario1)
        db.session.add(usuario2)      
        db.session.add(usuario3)
        
        db.session.commit()

        print("Usuários adicionados com sucesso:", usuario1.nome, "e", usuario2.nome)

        # --- Criar Autores ---
        autor1 = Autores(nome="Andrew S. Tanenbaum")         # Redes, Sistemas Operacionais
        autor2 = Autores(nome="Robert C. Martin")            # Engenharia de Software, Clean Code
        autor3 = Autores(nome="Thomas H. Cormen")            # Algoritmos (CLRS)
        autor4 = Autores(nome="Ian Goodfellow")              # Inteligência Artificial, Deep Learning
        autor5 = Autores(nome="Donald E. Knuth")             # Estruturas de Dados, The Art of Computer Programming


        db.session.add_all([autor1, autor2, autor3, autor4, autor5])
        db.session.commit()

        print("Autores adicionados com sucesso:", autor1.nome, "e", autor2.nome, "e", autor3.nome)

        # --- Criar Livros ---
        livro1 = Livros(
            titulo="Redes de Computadores",
            ano_publicacao=date(2011, 3, 1),
            categoria="Redes de Computadores",
            isbn="978-85-7522-123-4",
            curso="Engenharia da Computação"
        )

        livro2 = Livros(
            titulo="Clean Code: A Handbook of Agile Software Craftsmanship",
            ano_publicacao=date(2008, 8, 1),
            categoria="Engenharia de Software",
            isbn="978-85-1234-567-8",
            curso="Ciência da Computação"
        )

        livro3 = Livros(
            titulo="Introduction to Algorithms",
            ano_publicacao=date(2009, 7, 31),
            categoria="Algoritmos",
            isbn="978-85-1234-569-2",
            curso="Engenharia de Software"
        )

        livro4 = Livros(
            titulo="Deep Learning",
            ano_publicacao=date(2016, 11, 18),
            categoria="Inteligência Artificial",
            isbn="978-85-1234-570-8",
            curso="Inteligência Artificial"
        )

        livro5 = Livros(
            titulo="The Art of Computer Programming",
            ano_publicacao=date(2011, 2, 1),
            categoria="Estruturas de Dados e Algoritmos",
            isbn="978-85-1234-571-5",
            curso="Ciência da Computação"
        )

        db.session.add_all([livro1, livro2, livro3, livro4, livro5])
        db.session.commit()

        #print("livros adicionados com sucesso:", livro1.titulo, "e", livro2.titulo)

        # --- Criar Livro_Autor ---
        # Livro 1: Redes de Computadores - Andrew S. Tanenbaum
        livro1.autores.append(autor1)

        # Livro 2: Clean Code - Robert C. Martin
        livro2.autores.append(autor2)

        # Livro 3: Introduction to Algorithms - Thomas H. Cormen
        livro3.autores.append(autor3)

        # Livro 4: Deep Learning - Ian Goodfellow
        livro4.autores.append(autor4)

        # Livro 5: The Art of Computer Programming - Donald E. Knuth
        livro5.autores.append(autor5)
        db.session.commit()

        # --- Criar Exemplares ---
        
        # Livro 1 (mais popular) - 3 exemplares
        exemplar1 = Exemplares(livro=livro1, numero_chamada="A1", estado=EstadoExemplar.DISPONIVEL)
        exemplar2 = Exemplares(livro=livro1, numero_chamada="A2", estado=EstadoExemplar.DISPONIVEL)
        exemplar3 = Exemplares(livro=livro1, numero_chamada="A3", estado=EstadoExemplar.DISPONIVEL)

        # Livro 2 - 2 exemplares
        exemplar4 = Exemplares(livro=livro2, numero_chamada="B1", estado=EstadoExemplar.DISPONIVEL)
        exemplar5 = Exemplares(livro=livro2, numero_chamada="B2", estado=EstadoExemplar.DISPONIVEL)

        # Livros 3,4,5 - 1 exemplar cada
        exemplar6 = Exemplares(livro=livro3, numero_chamada="C1", estado=EstadoExemplar.DISPONIVEL)
        exemplar7 = Exemplares(livro=livro4, numero_chamada="D1", estado=EstadoExemplar.DISPONIVEL)
        exemplar8 = Exemplares(livro=livro5, numero_chamada="E1", estado=EstadoExemplar.DISPONIVEL)

        db.session.add_all([exemplar1, exemplar2, exemplar3, exemplar4, exemplar5, exemplar6, exemplar7, exemplar8])
        db.session.commit()


        # --- Criar Empréstimos --- 
        emprestimo1 = Emprestimos(
            usuario=usuario1,
            exemplar=exemplar1,
            data_emprestimo=date.today() - timedelta(days=10),
            data_devolucao=date.today() + timedelta(days=7),
            devolvido=False
        )

        emprestimo2 = Emprestimos(
            usuario=usuario2,
            exemplar=exemplar2,
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
    
# Rota padrão
@app.route('/')
def index():
    return render_template('login.html')

@app.route("/index")
def home():
    token = request.cookies.get('token') 
    if not token or not verificar_token(token):
        return redirect(url_for("auth.login"))  

    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True)
