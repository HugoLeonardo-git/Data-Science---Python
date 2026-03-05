import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("❌ MONGO_URI não encontrada no .env")

# Cliente Mongo
client = MongoClient(MONGO_URI)

# Banco
db = client["receitas_db"]

from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI"))

db = client["receitas_db"]

# cria índice único
db["receitas"].create_index("video_url", unique=True)

def get_database():
    return db

def get_collection(nome_collection: str):
    """
    Retorna uma collection do MongoDB.
    """
    return db[nome_collection]