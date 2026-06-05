"""
alerts.py
Génération des alertes météo
"""

import psycopg2
from scripts.utils import setup_logger, load_config

# Logger
logger = setup_logger("alerts")


# ============================================================
# GÉNÉRATION DES ALERTES
# ============================================================

def generate_alerts(**context) -> list:
    """
    Analyse les données et génère des alertes

    Types d'alertes :
    🔴 CANICULE   : température > 35°C
    🔵 FROID      : température < 10°C
    🌧️ PLUIE FORTE : précipitations > 20mm

    Retourne la liste des alertes générées
    """
    logger.info("🚨 Début génération des alertes")

    config = load_config()
    db     = config['database']
    seuils = config['alerts']

    conn = psycopg2.connect(
        host     = db['host'],
        port     = db['port'],
        dbname   = db['name'],
        user     = db['user'],
        password = db['password']
    )

    alerts = []

    try:
        alerts += detect_heat_alerts(conn, seuils['heat_threshold'])
        alerts += detect_cold_alerts(conn, seuils['cold_threshold'])
        alerts += detect_rain_alerts(conn, seuils['rain_threshold'])

        logger.info(f"✅ {len(alerts)} alerte(s) générée(s)")

        # Stocker les alertes pour la task suivante
        if context:
            context['ti'].xcom_push(key='alerts', value=alerts)

        return alerts

    finally:
        conn.close()


# ============================================================
# DÉTECTION ALERTES CANICULE
# ============================================================

def detect_heat_alerts(conn, threshold: float) -> list:
    """
    Détecte les villes avec température > threshold
    """
    sql = f"""
    SELECT
        city,
        MAX(temperature)  as max_temp,
        DATE(datetime)    as date
    FROM raw_weather
    WHERE
        temperature > {threshold}
    AND datetime >= NOW() - INTERVAL '6 hours'
    GROUP BY city, DATE(datetime);
    """

    alerts = []
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

            for row in rows:
                alert = {
                    "type"       : "CANICULE",
                    "city"       : row[0],
                    "value"      : row[1],
                    "date"       : str(row[2]),
                    "message"    : f"🔴 CANICULE à {row[0]} : {row[1]}°C",
                    "severity"   : "HIGH"
                }
                alerts.append(alert)
                logger.warning(alert['message'])

    except Exception as e:
        logger.error(f"❌ Erreur détection canicule : {e}")

    return alerts


# ============================================================
# DÉTECTION ALERTES FROID
# ============================================================

def detect_cold_alerts(conn, threshold: float) -> list:
    """
    Détecte les villes avec température < threshold
    """
    sql = f"""
    SELECT
        city,
        MIN(temperature)  as min_temp,
        DATE(datetime)    as date
    FROM raw_weather
    WHERE
        temperature < {threshold}
    AND datetime >= NOW() - INTERVAL '6 hours'
    GROUP BY city, DATE(datetime);
    """

    alerts = []
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

            for row in rows:
                alert = {
                    "type"    : "FROID",
                    "city"    : row[0],
                    "value"   : row[1],
                    "date"    : str(row[2]),
                    "message" : f"🔵 FROID à {row[0]} : {row[1]}°C",
                    "severity": "MEDIUM"
                }
                alerts.append(alert)
                logger.warning(alert['message'])

    except Exception as e:
        logger.error(f"❌ Erreur détection froid : {e}")

    return alerts


# ============================================================
# DÉTECTION ALERTES PLUIE
# ============================================================

def detect_rain_alerts(conn, threshold: float) -> list:
    """
    Détecte les villes avec précipitations > threshold
    """
    sql = f"""
    SELECT
        city,
        SUM(precipitation) as total_rain,
        DATE(datetime)     as date
    FROM raw_weather
    WHERE
        precipitation > 0
    AND datetime >= NOW() - INTERVAL '6 hours'
    GROUP BY city, DATE(datetime)
    HAVING SUM(precipitation) > {threshold};
    """

    alerts = []
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

            for row in rows:
                alert = {
                    "type"    : "PLUIE_FORTE",
                    "city"    : row[0],
                    "value"   : row[1],
                    "date"    : str(row[2]),
                    "message" : f"🌧️ PLUIE FORTE à {row[0]} : {row[1]}mm",
                    "severity": "MEDIUM"
                }
                alerts.append(alert)
                logger.warning(alert['message'])

    except Exception as e:
        logger.error(f"❌ Erreur détection pluie : {e}")

    return alerts


# ============================================================
# ENVOI NOTIFICATIONS
# ============================================================

def send_notifications(**context) -> None:
    """
    Envoie les notifications pour les alertes
    (logs pour l'instant, Slack/Email possible)
    """
    alerts = context['ti'].xcom_pull(
        task_ids = 'generate_alerts',
        key      = 'alerts'
    )

    if not alerts:
        logger.info("✅ Aucune alerte à notifier")
        return

    logger.info(f"📢 Envoi de {len(alerts)} notification(s)")

    for alert in alerts:
        logger.warning(f"🚨 ALERTE : {alert['message']}")

    # TODO : Ajouter email/Slack/Telegram ici
    logger.info("✅ Notifications envoyées (logs)")