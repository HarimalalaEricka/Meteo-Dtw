"""
extract.py
Récupération des données météo depuis open-meteo.com
"""

import requests
import json
from datetime import datetime, timedelta
from scripts.utils import setup_logger, load_config, format_datetime

# Logger
logger = setup_logger("extract")


# ============================================================
# FONCTION PRINCIPALE D'EXTRACTION
# ============================================================

def extract_weather_data(**context) -> list:
    """
    Récupère les données météo pour toutes les villes
    configurées dans config.yaml

    Retourne une liste de dictionnaires météo
    """
    logger.info("🌍 Début extraction données météo")

    # Charger la configuration
    config = load_config()

    cities      = config['cities']
    api_config  = config['api']
    params_config = config['weather_params']

    all_weather_data = []

    # -------------------------------------------------------
    # BOUCLE SUR CHAQUE VILLE
    # -------------------------------------------------------
    for city in cities:
        logger.info(f"📍 Extraction ville : {city['name']}")

        try:
            city_data = fetch_city_weather(
                city       = city,
                api_config = api_config,
                params     = params_config
            )

            if city_data:
                all_weather_data.extend(city_data)
                logger.info(
                    f"✅ {city['name']} : {len(city_data)} enregistrements récupérés"
                )
            else:
                logger.warning(f"⚠️ {city['name']} : aucune donnée reçue")

        except Exception as e:
            logger.error(f"❌ Erreur extraction {city['name']} : {e}")
            # On continue avec les autres villes
            continue

    logger.info(
        f"🏁 Extraction terminée : {len(all_weather_data)} enregistrements total"
    )

    # Pousser les données vers XCom pour la task suivante
    if context:
        context['ti'].xcom_push(key='weather_data', value=all_weather_data)

    return all_weather_data


# ============================================================
# FONCTION APPEL API PAR VILLE
# ============================================================

def fetch_city_weather(city: dict, api_config: dict, params: dict) -> list:
    """
    Appelle l'API open-meteo pour une ville spécifique

    Args:
        city       : dict avec name, latitude, longitude
        api_config : paramètres API (url, timeout, retry)
        params     : paramètres météo à récupérer

    Returns:
        liste de dictionnaires avec données météo horaires
    """

    # -------------------------------------------------------
    # CONSTRUCTION DE L'URL
    # -------------------------------------------------------
    # open-meteo : données des dernières 24h
    today     = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    api_params = {
        "latitude"  : city['latitude'],
        "longitude" : city['longitude'],
        "hourly"    : ",".join(params['hourly']),
        "start_date": yesterday,
        "end_date"  : today,
        "timezone"  : "Indian/Antananarivo"
    }

    # -------------------------------------------------------
    # APPEL API AVEC RETRY
    # -------------------------------------------------------
    max_retries = api_config.get('retry_count', 3)
    timeout     = api_config.get('timeout', 30)

    for attempt in range(1, max_retries + 1):
        try:
            logger.info(
                f"   🔄 Tentative {attempt}/{max_retries} pour {city['name']}"
            )

            response = requests.get(
                url     = api_config['base_url'],
                params  = api_params,
                timeout = timeout
            )

            # Vérifier le statut HTTP
            response.raise_for_status()

            # Vérifier que la réponse n'est pas vide
            if not response.content:
                raise ValueError("Réponse API vide")

            data = response.json()

            # Parser et retourner les données
            return parse_api_response(data, city['name'])

        except requests.exceptions.Timeout:
            logger.warning(
                f"   ⏱️ Timeout tentative {attempt} pour {city['name']}"
            )
            if attempt == max_retries:
                logger.error(
                    f"   ❌ Échec après {max_retries} tentatives (Timeout)"
                )
                return []

        except requests.exceptions.ConnectionError:
            logger.warning(
                f"   🔌 Erreur connexion tentative {attempt} pour {city['name']}"
            )
            if attempt == max_retries:
                logger.error(
                    f"   ❌ Échec après {max_retries} tentatives (Connexion)"
                )
                return []

        except requests.exceptions.HTTPError as e:
            logger.error(f"   ❌ Erreur HTTP {e} pour {city['name']}")
            return []

        except Exception as e:
            logger.error(f"   ❌ Erreur inattendue : {e}")
            return []

    return []


# ============================================================
# PARSING DE LA RÉPONSE API
# ============================================================

def parse_api_response(data: dict, city_name: str) -> list:
    """
    Parse la réponse JSON de open-meteo
    Retourne une liste de records météo

    Structure open-meteo :
    {
        "hourly": {
            "time": ["2024-01-01T00:00", ...],
            "temperature_2m": [25.0, ...],
            "relativehumidity_2m": [80, ...],
            "windspeed_10m": [10.0, ...],
            "precipitation": [0.0, ...],
            "weathercode": [0, ...]
        }
    }
    """

    if 'hourly' not in data:
        logger.error(f"❌ Clé 'hourly' absente dans la réponse pour {city_name}")
        return []

    hourly = data['hourly']
    times  = hourly.get('time', [])

    records = []

    for i, time_str in enumerate(times):
        try:
            record = {
                "city"        : city_name,
                "datetime"    : time_str,
                "temperature" : safe_get(hourly, 'temperature_2m', i),
                "humidity"    : safe_get(hourly, 'relativehumidity_2m', i),
                "wind_speed"  : safe_get(hourly, 'windspeed_10m', i),
                "precipitation": safe_get(hourly, 'precipitation', i),
                "weather_code": safe_get(hourly, 'weathercode', i),
                "raw_json"    : json.dumps({
                    "temperature" : safe_get(hourly, 'temperature_2m', i),
                    "humidity"    : safe_get(hourly, 'relativehumidity_2m', i),
                    "wind_speed"  : safe_get(hourly, 'windspeed_10m', i),
                    "precipitation": safe_get(hourly, 'precipitation', i),
                    "weather_code": safe_get(hourly, 'weathercode', i),
                }),
                "ingested_at" : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            records.append(record)

        except Exception as e:
            logger.warning(f"⚠️ Erreur parsing ligne {i} pour {city_name} : {e}")
            continue

    return records


def safe_get(data: dict, key: str, index: int):
    """
    Récupère une valeur de manière sécurisée
    Retourne None si absent ou index hors limite
    """
    values = data.get(key, [])
    if values and index < len(values):
        return values[index]
    return None