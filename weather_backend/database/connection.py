"""
connection.py
Gestion de la connexion PostgreSQL
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "postgres"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "weather_db"),
    "user": os.getenv("DB_USER", "airflow"),
    "password": os.getenv("DB_PASSWORD", "airflow"),
}


def get_connection():
    """Ouvre une connexion PostgreSQL avec curseur en dict (RealDictCursor)."""
    try:
        conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
        return conn
    except psycopg2.OperationalError as e:
        raise ConnectionError(f"❌ Impossible de se connecter à PostgreSQL : {e}")


def execute_query(query: str, params: tuple = None) -> list[dict]:
    """Exécute une requête SELECT et retourne une liste de dicts."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            return cur.fetchall()
    finally:
        conn.close()