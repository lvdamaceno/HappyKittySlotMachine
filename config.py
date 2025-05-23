import os
from dotenv import load_dotenv

# Carrega variáveis definidas em .env
load_dotenv()

class Config:
    # Chave usada por Flask para sessões e CSRF
    SECRET_KEY = os.getenv('SECRET_KEY', 'alterar_esta_chave_em_producao')

    # URL de conexão com o banco PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///slot.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configurações adicionais
    # Exemplo: número máximo de tentativas por usuário
    MAX_ATTEMPTS = int(os.getenv('MAX_ATTEMPTS', 10))
    STARTING_COINS = int(os.getenv('STARTING_COINS', 1000))