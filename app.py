from app import create_app
from app import db
#from app import bp

app = create_app()
#app.register_blueprint(bp) 

with app.app_context():
    print("↓ Verificando tabelas existentes...")
    inspector = db.inspect(db.engine)
    print("Tabelas antes:", inspector.get_table_names())
    
    db.create_all()  # Cria as tabelas
    
    print("Tabelas depois:", inspector.get_table_names())
    if 'usuario' in inspector.get_table_names():
        print("Tabela 'usuario' criada com sucesso!")
    else:
        print("Falha ao criar tabela")

if __name__ == "__main__":
    app.run(debug=True)