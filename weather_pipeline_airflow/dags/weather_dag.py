"""
weather_dag.py
DAG principal du pipeline météo
Orchestration complète toutes les 3 heures
"""

from airflow import DAG
from airflow.operators.python   import PythonOperator
from airflow.operators.bash     import BashOperator
from airflow.utils.dates        import days_ago
from datetime                   import datetime, timedelta

# Import des scripts
from scripts.extract  import extract_weather_data
from scripts.load     import load_raw_weather
from scripts.validate import validate_raw_data
from scripts.alerts   import generate_alerts, send_notifications


# ============================================================
# CONFIGURATION DU DAG
# ============================================================

default_args = {
    'owner'             : 'data_engineer',
    'depends_on_past'   : False,
    'start_date'        : datetime(2024, 1, 1),
    'email_on_failure'  : False,
    'email_on_retry'    : False,
    'retries'           : 3,
    'retry_delay'       : timedelta(minutes=5),
}

dag = DAG(
    dag_id            = 'weather_pipeline',
    default_args      = default_args,
    description       = '🌤️ Pipeline météo complet - extraction, stockage, transformation, alertes',
    schedule_interval = '0 */3 * * *',   # Toutes les 3 heures
    catchup           = False,
    tags              = ['weather', 'etl', 'production'],
)


# ============================================================
# TASK 1 — EXTRACTION API MÉTÉO
# ============================================================

task_extract = PythonOperator(
    task_id         = 'extract_weather_data',
    python_callable = extract_weather_data,
    dag             = dag,
    doc_md          = """
    ## 🌍 Extract Weather Data
    Appelle l'API open-meteo pour toutes les villes configurées.
    Gère les erreurs, retries et timeouts.
    """
)


# ============================================================
# TASK 2 — CHARGEMENT POSTGRESQL
# ============================================================

task_load = PythonOperator(
    task_id         = 'load_raw_weather',
    python_callable = load_raw_weather,
    dag             = dag,
    doc_md          = """
    ## 💾 Load Raw Weather
    Insère les données dans la table raw_weather.
    Gère les doublons avec ON CONFLICT DO NOTHING.
    """
)


# ============================================================
# TASK 3 — VALIDATION QUALITÉ
# ============================================================

task_validate = PythonOperator(
    task_id         = 'validate_raw_data',
    python_callable = validate_raw_data,
    dag             = dag,
    doc_md          = """
    ## ✅ Validate Raw Data
    Vérifie la qualité des données :
    - Pas de nulls critiques
    - Températures réalistes
    - Données récentes présentes
    """
)


# ============================================================
# TASK 4 — DÉCLENCHEMENT DBT MODELS
# ============================================================

task_dbt_run = BashOperator(
    task_id      = 'run_dbt_models',
    bash_command = """
        cd /opt/airflow/dbt_project && \
        dbt run \
            --profiles-dir /opt/airflow/dbt_project \
            --project-dir  /opt/airflow/dbt_project \
            --target prod
    """,
    dag = dag,
    doc_md = """
    ## ⚙️ Run dbt Models
    Déclenche les transformations dbt :
    - staging layer (nettoyage)
    - marts (fact + dim tables)
    - analytics (KPI météo)
    """
)


# ============================================================
# TASK 5 — DÉCLENCHEMENT DBT TESTS
# ============================================================

task_dbt_test = BashOperator(
    task_id      = 'run_dbt_tests',
    bash_command = """
        cd /opt/airflow/dbt_project && \
        dbt test \
            --profiles-dir /opt/airflow/dbt_project \
            --project-dir  /opt/airflow/dbt_project \
            --target prod
    """,
    dag = dag,
    doc_md = """
    ## 🧪 Run dbt Tests
    Vérifie la qualité via dbt :
    - not null
    - unique
    - relationships
    """
)


# ============================================================
# TASK 6 — GÉNÉRATION ALERTES
# ============================================================

task_alerts = PythonOperator(
    task_id         = 'generate_alerts',
    python_callable = generate_alerts,
    dag             = dag,
    doc_md          = """
    ## 🚨 Generate Alerts
    Détecte et génère les alertes :
    - 🔴 Canicule (> 35°C)
    - 🔵 Froid (< 10°C)
    - 🌧️ Pluie forte (> 20mm)
    """
)


# ============================================================
# TASK 7 — ENVOI NOTIFICATIONS
# ============================================================

task_notify = PythonOperator(
    task_id         = 'send_notifications',
    python_callable = send_notifications,
    dag             = dag,
    doc_md          = """
    ## 📢 Send Notifications
    Envoie les alertes via logs / email / Slack
    """
)


# ============================================================
# ORDRE D'EXÉCUTION DU DAG
# ============================================================

task_extract >> task_load >> task_validate >> task_dbt_run >> task_dbt_test >> task_alerts >> task_notify