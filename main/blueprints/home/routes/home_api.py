from flask import Blueprint, request, redirect, url_for, render_template
from ..utils import verificar_token  
from main.models import Livros, Emprestimos, Exemplares, Reservas, Autores, Usuario
from flask import jsonify
from sqlalchemy import or_, cast, String, Integer, extract
from sqlalchemy.orm import joinedload


home_bp = Blueprint('home', __name__)  

# Mapeia nome tabela para modelo e campos a pesquisar
TABELAS_MAPA = {
    "livros": (Livros, ["titulo", "autor"]),
    "exemplares": (Exemplares, ["id", "codigo"]),
    "usuarios": (Usuario, ["nome", "matricula"]),
    "emprestimos": (Emprestimos, ["id", "usuario_id"]),
    "autores": (Autores, ["nome"]),
    "reservas": (Reservas, ["id", "usuario_id"]),
}

@home_bp.route('/')
def index():
    token = request.cookies.get('token')
    if not token or not verificar_token(token):
        return redirect(url_for('auth.login'))  
    return render_template('index.html')

@home_bp.route('/consultar', methods=['GET'])
def consultar():
    # valida token, etc
    return render_template('consultar.html')

@home_bp.route('/consultar/buscar', methods=['POST'])
def buscar_simples():
    try:
        data = request.get_json()
        texto = data.get("texto", "").strip()
        tipo = data.get("tipo", "exemplares").lower()  # padrão buscar exemplares
        print(f"🔍 Texto recebido: '{texto}', Tipo: '{tipo}'")

        resultados = []

        print(f"Recebido tipo para busca: {tipo}")


        if tipo == "exemplares":
            exemplares = Exemplares.query \
                .join(Livros) \
                .outerjoin(Livros.autores) \
                .filter(
                    or_(
                        Exemplares.numero_chamada.ilike(f"%{texto}%"),
                        cast(Exemplares.estado, String).ilike(f"%{texto}%"),
                        Livros.titulo.ilike(f"%{texto}%"),
                        Livros.categoria.ilike(f"%{texto}%"),
                        cast(Livros.ano_publicacao, String).ilike(f"%{texto}%"),
                        Autores.nome.ilike(f"%{texto}%")
                    )
                ) \
                .options(joinedload(Exemplares.livro).joinedload(Livros.autores)) \
                .limit(50).all()

            print(f"📦 Número de exemplares encontrados: {len(exemplares)}")

            for ex in exemplares:
                resultados.append({
                    "id": ex.id,
                    "numero_chamada": ex.numero_chamada,
                    "estado": ex.estado.value,
                    "livro": {
                        "titulo": ex.livro.titulo,
                        "autores": [a.nome for a in ex.livro.autores],
                        "ano": ex.livro.ano_publicacao.strftime('%Y'),
                        "categoria": ex.livro.categoria
                    }
                })

        elif tipo == "livros":
            livros = Livros.query \
                .outerjoin(Livros.autores) \
                .filter(
                    or_(
                        Livros.titulo.ilike(f"%{texto}%"),
                        Livros.categoria.ilike(f"%{texto}%"),
                        Autores.nome.ilike(f"%{texto}%")
                    )
                ) \
                .options(joinedload(Livros.autores), joinedload(Livros.exemplares)) \
                .distinct() \
                .limit(50).all()

            print(f"📦 Número de livros encontrados: {len(livros)}")
            
            for livro in livros:
                print(f"📅 Ano original do livro (id={livro.id}):", livro.ano_publicacao)
                resultados.append({
                    "id": livro.id,
                    "titulo": livro.titulo,
                    "autores": [a.nome for a in livro.autores],
                    "ano_publicacao": livro.ano_publicacao.strftime('%Y') if livro.ano_publicacao else "N/A",
                    "categoria": livro.categoria or "N/A",
                    "quantidade_exemplares": len(livro.exemplares)
                })

        elif tipo == "usuarios":
            usuarios = Usuario.query.filter(
                or_(
                    Usuario.nome.ilike(f"%{texto}%"),
                    cast(Usuario.matricula, String).ilike(f"%{texto}%"),
                    Usuario.email.ilike(f"%{texto}%"),
                    Usuario.telefone.ilike(f"%{texto}%")
                )
            ).limit(50).all()

            print(f"📦 Número de usuários encontrados: {len(usuarios)}")

            for usuario in usuarios:
                resultados.append({
                    "id": usuario.id,
                    "nome": usuario.nome,
                    "matricula": usuario.matricula,
                    "email": usuario.email,
                    "telefone": usuario.telefone
                })
        elif tipo == "emprestimos":
            emprestimos = Emprestimos.query \
                .join(Usuario) \
                .join(Exemplares) \
                .join(Livros, Exemplares.livro) \
                .filter(
                    or_(
                        Usuario.nome.ilike(f"%{texto}%"),
                        cast(Usuario.matricula, String).ilike(f"%{texto}%"),
                        Livros.titulo.ilike(f"%{texto}%")
                    )
                ) \
                .options(
                    joinedload(Emprestimos.usuario),
                    joinedload(Emprestimos.exemplar).joinedload(Exemplares.livro)
                ) \
                .limit(50).all()

            print(f"📦 Número de empréstimos encontrados: {len(emprestimos)}")

            for emp in emprestimos:
                resultados.append({
                    "id": emp.id,
                    "livro": {
                        "titulo": emp.exemplar.livro.titulo
                    },
                    "usuario": {
                        "nome": emp.usuario.nome,
                        "matricula": emp.usuario.matricula
                    },
                    "data_emprestimo": emp.data_emprestimo.strftime('%d/%m/%Y'),
                    "data_devolucao": emp.data_devolucao.strftime('%d/%m/%Y')
                })

        elif tipo == "autores":
            autores = Autores.query \
                .filter(Autores.nome.ilike(f"%{texto}%")) \
                .limit(50).all()

            print(f"📦 Número de autores encontrados: {len(autores)}")

            for autor in autores:
                resultados.append({
                    "nome": autor.nome
                })
        
        elif tipo == "reservas":
            reservas = Reservas.query \
                .join(Reservas.exemplar) \
                .join(Exemplares.livro) \
                .join(Reservas.usuario) \
                .filter(
                    or_(
                        Livros.titulo.ilike(f"%{texto}%"),
                        Usuario.nome.ilike(f"%{texto}%"),
                        cast(Reservas.status, String).ilike(f"%{texto}%")
                    )
                ) \
                .limit(50).all()

            

            for reserva in reservas:
                print(f"📦 Número de reservas encontradas: {(reserva.exemplar.livro.titulo)}")
                print(f"📦 Número de reservas encontradas: {(reserva.usuario.nome)}")
                print(f"📦 Número de reservas encontradas: {(reserva.status.name)}")

                resultados.append({

                    "livro": {
                        "titulo": reserva.exemplar.livro.titulo
                    },

                    #"livro": reserva.exemplar.livro.titulo,

                    "usuario": {
                        "nome": reserva.usuario.nome,
                        "matricula": reserva.usuario.matricula
                    },

                    #"usuario": f"{reserva.usuario.nome} ({reserva.usuario.matricula})",
                    "status": reserva.status.name  # ou .value dependendo do Enum
                })

        else:
            return jsonify({"erro": "Tipo inválido. Use 'exemplares' ou 'livros'."}), 400

        return jsonify(resultados)

    except Exception as e:
        print("❌ ERRO NA BUSCA:", e)
        return jsonify({"erro": str(e)}), 500


@home_bp.route('/consultar/exemplares', methods=['GET'])
def listar_exemplares():
    exemplares = Exemplares.query.limit(20).all()
    return jsonify([ex.to_dict() for ex in exemplares])

@home_bp.route('/consultar/livros', methods=['GET'])
def listar_livros():
    livros = Livros.query.all()
    resultado = []

    for livro in livros:
        resultado.append({
            "id": livro.id,
            "titulo": livro.titulo,
            "categoria": livro.categoria,
            "ano_publicacao": livro.ano_publicacao.strftime('%Y'),
            "isbn": livro.isbn,
            "curso": livro.curso,
            "autores": [autor.nome for autor in livro.autores],
            "quantidade_exemplares": len(livro.exemplares)
        })

    return jsonify(resultado)

@home_bp.route('/consultar/usuarios', methods=['GET'])
def consultar_usuarios():
    usuarios = Usuario.query.all()
    lista = []
    for u in usuarios:
        lista.append({
            "id": u.id,
            "nome": u.nome,
            "cpf": u.cpf,
            "email": u.email,
            "telefone": u.telefone,
            "data_nascimento": u.data_nascimento.strftime('%Y-%m-%d'),
            "cargo": u.cargo.value,
            "matricula": u.matricula
        })
    return jsonify(lista)

@home_bp.route('/consultar/emprestimos', methods=['GET'])
def consultar_emprestimos():
    emprestimos = Emprestimos.query.all()
    lista = []
    for e in emprestimos:
        lista.append({
            "id": e.id,
            "usuario": {
                "nome": e.usuario.nome,
                "matricula": e.usuario.matricula,
            },
            "livro": {
                "titulo": e.exemplar.livro.titulo,
                "numero_chamada": e.exemplar.numero_chamada,
            },
            "data_emprestimo": e.data_emprestimo.strftime('%d/%m/%Y'),
            "data_devolucao": e.data_devolucao.strftime('%d/%m/%Y') if e.data_devolucao else None,
            "devolvido": e.devolvido
        })
    return jsonify(lista)

@home_bp.route('/consultar/autores', methods=['GET'])
def consultar_autores():
    autores = Autores.query.all()
    lista_autores = []
    for autor in autores:
        lista_autores.append({
            'id': autor.id,
            'nome': autor.nome
            # adicione outros campos se quiser
        })
    return jsonify(lista_autores)

@home_bp.route("/consultar/reservas", methods=['GET'])
def consultar_reservas():
    reservas = Reservas.query.join(Exemplares).join(Livros).join(Usuario).all()
    
    resultado = []
    for reserva in reservas:
        resultado.append({
            "id": reserva.id,
            "data_reserva": reserva.data_reserva.strftime("%d/%m/%Y"),
            "status": reserva.status.name,  # Exemplo: 'ATIVA'
            "usuario": {
                "nome": reserva.usuario.nome,
                "matricula": reserva.usuario.matricula,
                "email": reserva.usuario.email,
                "telefone": reserva.usuario.telefone,
            },
            "exemplar": {
                "numero_chamada": reserva.exemplar.numero_chamada,
                "livro": {
                    "titulo": reserva.exemplar.livro.titulo,
                    "categoria": reserva.exemplar.livro.categoria,
                    "ano_publicacao": reserva.exemplar.livro.ano_publicacao.strftime("%Y"),
                }
            }
        })
    
    return {"reservas": resultado}

@home_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    token = request.cookies.get('token')
    if not token or not verificar_token(token):
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        # aqui processa o cadastro do livro
        titulo = request.form['titulo']
        autor_nome = request.form['autor']
        ano = request.form['ano']
        categoria = request.form['categoria']

        '''
        # salvar no banco (exemplo simplificado)
        # verifique se o autor já existe, se não, cria novo autor
        autor = Autores.query.filter_by(nome=autor_nome).first()
        if not autor:
            autor = Autores(nome=autor_nome)
            db.session.add(autor)

        livro = Livros(
            titulo=titulo,
            ano_publicacao=ano,
            categoria=categoria,
            isbn="",  # pode adicionar no form depois
            curso=""  # idem
        )
        livro.autores.append(autor)
        db.session.add(livro)
        db.session.commit()

        return redirect(url_for('home.index'))
        '''

    return render_template('cadastrar.html')

@home_bp.route('/editar')
def editar():
    token = request.cookies.get('token')
    if not token or not verificar_token(token):
        return redirect(url_for('auth.login'))
    return render_template('editar.html')

@home_bp.route('/excluir', methods=['GET', 'POST'], endpoint='excluir_livro')
def excluir():
    token = request.cookies.get('token')
    if not token or not verificar_token(token):
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        # buscar e excluir livro aqui

    return render_template('excluir.html')

