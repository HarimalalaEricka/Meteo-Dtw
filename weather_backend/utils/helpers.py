"""
helpers.py
Fonctions utilitaires partagées
"""
from fastapi import HTTPException


def ensure_city_exists(city: str, is_valid_city_fn):
    """Lève une 404 propre si la ville n'existe pas dans dim_city."""
    if city and not is_valid_city_fn(city):
        raise HTTPException(status_code=404, detail=f"Ville '{city}' introuvable")


def handle_db_error(e: Exception):
    """Convertit une erreur de connexion DB en réponse HTTP 503."""
    raise HTTPException(status_code=503, detail=f"Erreur base de données : {str(e)}")