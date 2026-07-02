"""
weather_dag.py
DAG principal du pipeline météo
Orchestration complète toutes les 3 heures
"""

from airflow import DAG
from airflow.operators.python   import PythonOperator
from airflow.operators.bash     import BashOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime                   import datetime, timedelta

# Import des scripts
from scripts.extract       import extract_weather_data
from scripts.load          import load_raw_weather
from scripts.validate      import validate_raw_data
from scripts.aggregations  import update_aggregations
from scripts.alerts        import generate_alerts, send_notifications


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
    description       = '🌤️ Pipeline météo complet',
    schedule_interval = '0 */3 * * *',
    catchup           = False,
    tags              = ['weather', 'etl', 'production'],
)


# ============================================================
# CHEMIN VERS LE DOSSIER DBT
# ============================================================
DBT_PROJECT_DIR = "/opt/airflow/dbt_project"


# ============================================================
# TASK 1 — EXTRACTION API MÉTÉO
# ============================================================
task_extract = PythonOperator(
    task_id         = 'extract_weather_data',
    python_callable = extract_weather_data,
    dag             = dag,
)


# ============================================================
# TASK 2 — CHARGEMENT POSTGRESQL
# ============================================================
task_load = PythonOperator(
    task_id         = 'load_raw_weather',
    python_callable = load_raw_weather,
    trigger_rule    = TriggerRule.ALL_SUCCESS,
    dag             = dag,
)


# ============================================================
# TASK 3 — VALIDATION QUALITÉ
# ============================================================
task_validate = PythonOperator(
    task_id         = 'validate_raw_data',
    python_callable = validate_raw_data,
    trigger_rule    = TriggerRule.ALL_SUCCESS,
    dag             = dag,
)

# ============================================================
# TASK 3.5 — DBT SEED (chargement des seeds CSV)
# ============================================================
task_dbt_seed = BashOperator(
    task_id      = 'run_dbt_seed',
    bash_command = f"""
        cd "{DBT_PROJECT_DIR}" && \
        dbt seed \
            --profiles-dir "{DBT_PROJECT_DIR}" \
            --project-dir  "{DBT_PROJECT_DIR}"
    """,
    trigger_rule = TriggerRule.ALL_SUCCESS,
    dag          = dag,
)

# ============================================================
# TASK 4 — DÉCLENCHEMENT DBT MODELS
# ============================================================
task_dbt_run = BashOperator(
    task_id      = 'run_dbt_models',
    bash_command = f"""
        cd "{DBT_PROJECT_DIR}" && \
        dbt run \
            --profiles-dir "{DBT_PROJECT_DIR}" \
            --project-dir  "{DBT_PROJECT_DIR}"
    """,
    trigger_rule = TriggerRule.ALL_SUCCESS,
    dag          = dag,
)


# ============================================================
# TASK 5 — DBT TESTS
# ============================================================
task_dbt_test = BashOperator(
    task_id      = 'run_dbt_tests',
    bash_command = f"""
        cd "{DBT_PROJECT_DIR}" && \
        dbt run \
            --profiles-dir "{DBT_PROJECT_DIR}" \
            --project-dir  "{DBT_PROJECT_DIR}"
    """,
    trigger_rule = TriggerRule.ALL_SUCCESS,
    dag          = dag,
)


# ============================================================
# TASK 6 — UPDATE AGGREGATIONS
# ============================================================
task_aggregations = PythonOperator(
    task_id         = 'update_aggregations',
    python_callable = update_aggregations,
    trigger_rule    = TriggerRule.ALL_SUCCESS,
    dag             = dag,
)


# ============================================================
# TASK 7 — GÉNÉRATION ALERTES
# ============================================================
task_alerts = PythonOperator(
    task_id         = 'generate_alerts',
    python_callable = generate_alerts,
    trigger_rule    = TriggerRule.ALL_SUCCESS,
    dag             = dag,
)


# ============================================================
# TASK 8 — ENVOI NOTIFICATIONS
# ============================================================
task_notify = PythonOperator(
    task_id         = 'send_notifications',
    python_callable = send_notifications,
    trigger_rule    = TriggerRule.ALL_DONE,
    dag             = dag,
)


# ============================================================
# ORDRE D'EXÉCUTION
# ============================================================
task_extract >> task_load >> task_validate >> task_dbt_seed >> task_dbt_run >> task_dbt_test >> task_aggregations >> task_alerts >> task_notify