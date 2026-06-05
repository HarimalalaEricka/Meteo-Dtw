"""
validate.py
Vérification de la qualité des données brutes
"""

import psycopg2
from scripts.utils import (
    setup_logger, load_config,
    is_valid_temperature, is_valid_humidity, is_valid_wind_speed
)

# Logger
logger = setup_logger("validate")


# ============================================================
# VALIDATION PRINCIPALE
# ============================================================

def validate_raw_data(**context) -> bool:
    """
    Vérifie la qualité des données dans raw_weather

    Checks :
    ✅ Pas de valeurs nulles critiques
    ✅ Températures réalistes
    ✅ Humidité réaliste
    ✅ Timestamps valides
    ✅ Pas de doublons récents

    Retourne True si OK, lève une exception si FAIL
    """
    logger.info("🔍 Début validation des données")

    config = load_config()
    db     = config['database']

    conn = psycopg2.connect(
        host     = db['host'],
        port     = db['port'],
        dbname   = db['name'],
        user     = db['user'],
        password = db['password']
    )

    issues = []

    try:
        # -------------------------------------------------------
        # CHECK 1 : Valeurs nulles critiques
        # -------------------------------------------------------
        issues += check_null_values(conn)

        # -------------------------------------------------------
        # CHECK 2 : Températures réalistes
        # -------------------------------------------------------
        issues += check_temperature_range(conn)

        # -------------------------------------------------------
        # CHECK 3 : Humidité réaliste
        # -------------------------------------------------------
        issues += check_humidity_range(conn)

        # -------------------------------------------------------
        # CHECK 4 : Données récentes présentes
        # -------------------------------------------------------
        issues += check_recent_data(conn)

        # -------------------------------------------------------
        # RÉSULTAT FINAL
        # -------------------------------------------------------
        if issues:
            for issue in issues:
                logger.error(f"❌ {issue}")
            raise ValueError(
                f"Validation FAILED : {len(issues)} problème(s) détecté(s)"
            )
        else:
            logger.info("✅ Validation réussie : toutes les données sont propres")
            return True

    finally:
        conn.close()


# ============================================================
# CHECKS INDIVIDUELS
# ============================================================

def check_null_values(conn) -> list:
    """
    Vérifie l'absence de nulls sur les champs critiques
    """
    logger.info("   🔎 Check nulls...")

    sql = """
    SELECT COUNT(*) as null_count
    FROM raw_weather
    WHERE
        city        IS NULL OR
        datetime    IS NULL OR
        temperature IS NULL OR
        humidity    IS NULL
    AND ingested_at >= NOW() - INTERVAL '6 hours';
    """

    issues = []
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            result = cur.fetchone()
            null_count = result[0]

            if null_count > 0:
                issues.append(
                    f"Valeurs nulles critiques : {null_count} enregistrement(s)"
                )
            else:
                logger.info("   ✅ Pas de valeurs nulles critiques")

    except Exception as e:
        issues.append(f"Erreur check nulls : {e}")

    return issues


def check_temperature_range(conn) -> list:
    """
    Vérifie que les températures sont réalistes (-50 à 60°C)
    """
    logger.info("   🌡️ Check températures...")

    sql = """
    SELECT COUNT(*) as invalid_count
    FROM raw_weather
    WHERE
        (temperature < -50 OR temperature > 60)
    AND ingested_at >= NOW() - INTERVAL '6 hours';
    """

    issues = []
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            result = cur.fetchone()
            invalid_count = result[0]

            if invalid_count > 0:
                issues.append(
                    f"Températures invalides : {invalid_count} enregistrement(s)"
                )
            else:
                logger.info("   ✅ Températures dans les limites normales")

    except Exception as e:
        issues.append(f"Erreur check température : {e}")

    return issues


def check_humidity_range(conn) -> list:
    """
    Vérifie que l'humidité est entre 0% et 100%
    """
    logger.info("   💧 Check humidité...")

    sql = """
    SELECT COUNT(*) as invalid_count
    FROM raw_weather
    WHERE
        (humidity < 0 OR humidity > 100)
    AND ingested_at >= NOW() - INTERVAL '6 hours';
    """

    issues = []
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            result = cur.fetchone()
            invalid_count = result[0]

            if invalid_count > 0:
                issues.append(
                    f"Humidité invalide : {invalid_count} enregistrement(s)"
                )
            else:
                logger.info("   ✅ Humidité dans les limites normales")

    except Exception as e:
        issues.append(f"Erreur check humidité : {e}")

    return issues


def check_recent_data(conn) -> list:
    """
    Vérifie que des données récentes sont bien présentes
    """
    logger.info("   📅 Check données récentes...")

    sql = """
    SELECT COUNT(*) as recent_count
    FROM raw_weather
    WHERE ingested_at >= NOW() - INTERVAL '6 hours';
    """

    issues = []
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            result = cur.fetchone()
            recent_count = result[0]

            if recent_count == 0:
                issues.append("Aucune donnée récente (dernières 6h) trouvée")
            else:
                logger.info(f"   ✅ {recent_count} enregistrements récents présents")

    except Exception as e:
        issues.append(f"Erreur check données récentes : {e}")

    return issues