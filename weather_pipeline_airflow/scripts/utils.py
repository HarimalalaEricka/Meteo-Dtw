"""
utils.py
Fonctions communes réutilisables
"""

import yaml
import logging
import os
from datetime import datetime

# ============================================================
# CONFIGURATION DU LOGGING
# ============================================================

def setup_logger(name: str) -> logging.Logger:
    """
    Crée un logger propre pour chaque script
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Format des logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Handler console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger


# ============================================================
# CHARGEMENT CONFIG
# ============================================================

def load_config() -> dict:
    """
    Charge le fichier config.yaml
    Retourne un dictionnaire de configuration
    """
    # Chemin vers config.yaml
    config_path = os.path.join(
        os.path.dirname(__file__),
        '..', 'config', 'config.yaml'
    )

    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        raise Exception(f"❌ config.yaml introuvable : {config_path}")
    except yaml.YAMLError as e:
        raise Exception(f"❌ Erreur lecture config.yaml : {e}")


# ============================================================
# FONCTIONS UTILITAIRES
# ============================================================

def format_datetime(dt_string: str) -> datetime:
    """
    Convertit une string en datetime
    Gère plusieurs formats possibles
    """
    formats = [
        "%Y-%m-%dT%H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(dt_string, fmt)
        except ValueError:
            continue

    raise ValueError(f"❌ Format datetime non reconnu : {dt_string}")


def is_valid_temperature(temp: float) -> bool:
    """
    Vérifie si une température est réaliste
    Entre -50°C et 60°C pour Madagascar
    """
    return -50 <= temp <= 60


def is_valid_humidity(humidity: float) -> bool:
    """
    Vérifie si l'humidité est réaliste
    Entre 0% et 100%
    """
    return 0 <= humidity <= 100


def is_valid_wind_speed(wind: float) -> bool:
    """
    Vérifie si la vitesse du vent est réaliste
    Entre 0 et 200 km/h
    """
    return 0 <= wind <= 200


def get_current_timestamp() -> str:
    """
    Retourne le timestamp actuel formaté
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def chunk_list(lst: list, chunk_size: int) -> list:
    """
    Divise une liste en morceaux
    Utile pour les insertions en batch
    """
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]