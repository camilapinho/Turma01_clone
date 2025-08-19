import sqlite3
import os

# Caminho relativo à pasta do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "sistema.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

