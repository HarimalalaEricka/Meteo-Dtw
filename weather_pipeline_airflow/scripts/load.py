"""
load.py
Insertion des données météo dans PostgreSQL (table raw_weather)
"""

import psycopg2
import psycopg2.extras
from scripts.utils import setup_logger, load_config, chunk_list

# Logger
logger = setup_logger("load")


# ============================================================
# CONNEXION POSTGRESQL
# ============================================================

def get_connection():
    """
    Crée une connexion PostgreSQL
    à partir de la config
    """
    config = load_config()
    db     = config['database']

    try:
        conn = psycopg2.connect(
            host     = db['host'],
            port     = db['port'],
            dbname   = db['name'],
            user     = db['user'],
            password = db['password']
        )
        logger.info("✅ Connexion PostgreSQL établie")
        return conn

    except psycopg2.OperationalError as e:
        logger.error(f"❌ Impossible de se connecter à PostgreSQL : {e}")
        raise


# ============================================================
# CRÉATION DE LA TABLE SI INEXISTANTE
# ============================================================

def create_raw_table_if_not_exists(conn):
    """
    Crée la table raw_weather si elle n'existe pas
    """
    sql_create = """
    CREATE TABLE IF NOT EXISTS raw_weather (
        id              SERIAL PRIMARY KEY,
        city            VARCHAR(100)    NOT NULL,
        datetime        TIMESTAMP       NOT NULL,
        temperature     FLOAT,
        humidity        FLOAT,
        wind_speed      FLOAT,
        precipitation   FLOAT,
        weather_code    INTEGER,
        raw_json        TEXT,
        ingested_at     TIMESTAMP       DEFAULT NOW(),

        -- Contrainte unicité pour éviter les doublons
        UNIQUE (city, datetime)
    );
    """

    try:
        with conn.cursor() as cursor:
            cursor.execute(sql_create)
        conn.commit()
        logger.info("✅ Table raw_weather prête")

    except Exception as e:
        conn.rollback()
        logger.error(f"❌ Erreur création table : {e}")
        raise


# ============================================================
# INSERTION DES DONNÉES
# ============================================================

def load_raw_weather(**context) -> int:
    """
    Insère les données météo dans raw_weather
    Gère les doublons avec ON CONFLICT DO NOTHING

    Retourne le nombre de lignes insérées
    """
    logger.info("💾 Début chargement données dans PostgreSQL")

    # Récupérer les données depuis XCom
    weather_data = context['ti'].xcom_pull(
        task_ids = 'extract_weather_data',
        key      = 'weather_data'
    )

    if not weather_data:
        logger.warning("⚠️ Aucune donnée à insérer")
        return 0

    logger.info(f"📊 {len(weather_data)} enregistrements à insérer")

    # Connexion
    conn = get_connection()

    try:
        # Créer la table si besoin
        create_raw_table_if_not_exists(conn)

        # Insérer par batch de 100
        total_inserted = 0
        for batch in chunk_list(weather_data, 100):
            inserted = insert_batch(conn, batch)
            total_inserted += inserted

        logger.info(
            f"✅ Chargement terminé : {total_inserted} lignes insérées"
        )
        return total_inserted

    except Exception as e:
        logger.error(f"❌ Erreur chargement : {e}")
        raise

    finally:
        conn.close()


def insert_batch(conn, batch: list) -> int:
    """
    Insère un batch de données dans raw_weather
    Ignore les doublons (ON CONFLICT DO NOTHING)
    """

    sql_insert = """
    INSERT INTO raw_weather (
        city,
        datetime,
        temperature,
        humidity,
        wind_speed,
        precipitation,
        weather_code,
        raw_json,
        ingested_at
    )
    VALUES (
        %(city)s,
        %(datetime)s,
        %(temperature)s,
        %(humidity)s,
        %(wind_speed)s,
        %(precipitation)s,
        %(weather_code)s,
        %(raw_json)s,
        %(ingested_at)s
    )
    ON CONFLICT (city, datetime) DO NOTHING;
    """

    try:
        with conn.cursor() as cursor:
            psycopg2.extras.execute_batch(
                cursor,
                sql_insert,
                batch,
                page_size = 100
            )
        conn.commit()

        logger.info(f"   ✅ Batch de {len(batch)} insérés")
        return len(batch)

    except Exception as e:
        conn.rollback()
        logger.error(f"   ❌ Erreur insertion batch : {e}")
        raise