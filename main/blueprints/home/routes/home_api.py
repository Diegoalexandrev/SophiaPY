from flask import Blueprint, request, redirect, url_for, render_template
from ..utils import verificar_token  
from main.models import Livros, Emprestimos, Exemplares, Reservas, Autores, Usuario
from flask import jsonify
from sqlalchemy import or_, cast, String, Integer, extract
from sqlalchemy.orm import joinedload
from main.database import db
from datetime import datetime
from main.models import Exemplares, EstadoExemplar
from main.blueprints.home.utils import PilhaLivros



home_bp = Blueprint('home', __name__)  
pilha_livros = PilhaLivros()

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
    return render_template('consultar.html')

@home_bp.route('/consultar/buscar', methods=['POST'])
def buscar_simples():
    try:
        data = request.get_json()
        texto = data.get("texto", "").strip()
        tipo = data.get("tipo", "exemplares").lower()  
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
                pilha_livros.push(livro.titulo)  # Empilhando o título
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

                    "usuario": {
                        "nome": reserva.usuario.nome,
                        "matricula": reserva.usuario.matricula
                    },
                    "status": reserva.status.name  
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
            "status": reserva.status.name,  
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

@home_bp.route('/cadastrar', methods=['GET'])
def cadastrar():
    token = request.cookies.get('token')
    if not token or not verificar_token(token):
        return redirect(url_for('auth.login'))

    autores = Autores.query.all()
    livros = Livros.query.all()  

    return render_template('cadastrar.html', autores=autores, livros=livros)


@home_bp.route('/cadastrar_livro', methods=['POST'])
def cadastrar_livro():
    token = request.cookies.get('token')
    if not token or not verificar_token(token):
        return redirect(url_for('auth.login'))

    titulo = request.form.get('titulo')
    ano_str = request.form.get('ano_publicacao')
    categoria = request.form.get('categoria')
    isbn = request.form.get('isbn')
    curso = request.form.get('curso')
    autores_ids = request.form.getlist('autores')

    try:
        ano_publicacao = datetime.strptime(ano_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        ano_publicacao = None

    livro = Livros(
        titulo=titulo,
        ano_publicacao=ano_publicacao,
        categoria=categoria,
        isbn=isbn,
        curso=curso
    )

    for autor_id in autores_ids:
        autor = Autores.query.get(autor_id)
        if autor:
            livro.autores.append(autor)

    db.session.add(livro)
    db.session.commit()

    return redirect(url_for('home.index'))

@home_bp.route('/cadastrar_autor', methods=['POST'])
def cadastrar_autor():
    token = request.cookies.get('token')
    if not token or not verificar_token(token):
        return redirect(url_for('auth.login'))

    nome_autor = request.form.get('nome_autor')

    if nome_autor:
        novo_autor = Autores(nome=nome_autor)
        db.session.add(novo_autor)
        db.session.commit()

    return redirect(url_for('home.index'))

@home_bp.route('/cadastrar_exemplar', methods=['POST'])
def cadastrar_exemplar():
    token = request.cookies.get('token')
    if not token or not verificar_token(token):
        return redirect(url_for('auth.login'))

    livro_id = request.form.get('livro_exemplar')
    numero_chamada = request.form.get('numero_chamada')
    estado = request.form.get('estado')

    if livro_id and numero_chamada and estado:
        livro = Livros.query.get(livro_id)
        if livro:
            novo_exemplar = Exemplares(
                livro_id=livro_id,
                numero_chamada=numero_chamada,
                estado=estado
            )
            db.session.add(novo_exemplar)
            db.session.commit()

    return redirect(url_for('home.index'))

@home_bp.route('/editar')
def editar():
    token = request.cookies.get('token')
    if not token or not verificar_token(token):
        return redirect(url_for('auth.login'))
    return render_template('editar.html')

@home_bp.route('/excluir_exemplar', methods=['POST'])
def excluir_exemplar():
    token = request.cookies.get('token')
    if not token or not verificar_token(token):
        return jsonify({"status": "unauthorized"})

    numero_chamada = request.form.get('numero_chamada', '').strip()
    exemplar = Exemplares.query.filter_by(numero_chamada=numero_chamada).first()

    if not exemplar:
        return jsonify({"status": "not_found"})

    if exemplar.estado != EstadoExemplar.DISPONIVEL:
        return jsonify({"status": "not_allowed", "message": "Só é permitido excluir exemplares DISPONÍVEIS."})

    
    if exemplar.emprestimos:
        return jsonify({"status": "in_use", "message": "Este exemplar já possui histórico de empréstimos e não pode ser excluído."})

    try:
        db.session.delete(exemplar)
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        print("Erro ao excluir exemplar:", e)
        return jsonify({"status": "error", "message": str(e)})


@home_bp.route('/excluir', methods=['GET'])
def excluir():
    token = request.cookies.get('token')
    if not token or not verificar_token(token):
        return redirect(url_for('auth.login'))
    return render_template('excluir.html') 

@home_bp.route('/consultar/pilha_livros', methods=['GET'])
def ver_pilha_livros():
    return jsonify(pilha_livros.listar())
