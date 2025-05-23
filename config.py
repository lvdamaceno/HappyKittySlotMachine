import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'alterar_em_producao')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///slot.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STARTING_COINS = int(os.getenv('STARTING_COINS', 1000))
    MAX_ATTEMPTS = int(os.getenv('MAX_ATTEMPTS', 10))
    COST_PER_PLAY = int(os.getenv('COST_PER_PLAY', 100))