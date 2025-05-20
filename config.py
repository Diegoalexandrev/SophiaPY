import os
from dotenv import load_dotenv

if not os.getenv('RENDER'):  # Se NÃO estiver no Render
    print("Rodando LOCALMENTE (desenvolvimento)")
else:
    print("Rodando no RENDER (produção)")

# Carrega variáveis do .env.local apenas em desenvolvimento
if not os.getenv('RENDER'):  
    load_dotenv('.env.local')

# Configuração do banco de dados
if os.getenv('RENDER'):  # Se estiver no Render (produção)
    DATABASE_URL = os.getenv('DATABASE_URL_INTERNO')  
else:  # Local (desenvolvimento)
    DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

#load_dotenv('.env.local')

#DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
SQLALCHEMY_DATABASE_URI = DATABASE_URL
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.getenv("SECRET_KEY")
