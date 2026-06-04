On a 5 dossiers:
    weather_pipeline_airflow
    weather_dbt
    weather_backend_api
    weather_frontend
    weather_visualisation

AIRFLOW
    ROLE : Airflow est le chef orchestrateur du pipeline meteo
        Il sert a :
            automatiser l’ingestion des données
            enchaîner les traitements
            déclencher dbt
            générer les alertes
            gérer le planning (toutes les 3h)

    STRUCTURE DU DOSSIER AIRFLOW :
        airflow_project/
        │
        ├── dags/
        │   └── weather_dag.py
        │
        ├── scripts/
        │   ├── extract.py
        │   ├── load.py
        │   ├── alerts.py
        │   └── utils.py
        │
        ├── config/
        │   └── config.yaml
        │
        ├── logs/
        │
        ├── plugins/
        │
        ├── requirements.txt
        │
        └── docker-compose.yml

    FONCTIONNALITES GLOBALES :
        ✔️ Automatisation
                exécution toutes les 3 heures
        ✔️ Ingestion API
                récupération météo
        ✔️ Stockage brut
                insertion PostgreSQL (raw_weather)
        ✔️ Transformation trigger
                lancement dbt
        ✔️ Data Quality
                vérification des données
        ✔️ Calcul alertes
                canicule / froid / pluie
        ✔️ Notifications (optionnel)
                email / logs / webhook

    TASK AIRFLOW (PIPELINE) :
        🟦 TASK 1 — Extract API météo
            📌 Nom :
            extract_weather_data

            🎯 Fonctionnalités :
            appel API météo ( utilise open-meteo.com)
            récupération JSON
            gestion erreurs API

            📤 Output :
            données météo en mémoire

        🟩 TASK 2 — Load raw PostgreSQL
            📌 Nom :
            load_raw_weather

            🎯 Fonctionnalités :
            insertion dans raw_weather
            gestion doublons
            mapping des champs

            📤 Output :
            données stockées brutes

        🟨 TASK 3 — Data Quality Check
            📌 Nom :
            validate_raw_data

            🎯 Fonctionnalités :
            vérifier nulls
            vérifier valeurs réalistes
            contrôler timestamps

            📤 Output :
            validation OK / FAIL

        🟧 TASK 4 — Run dbt models( le eto declencheur anle dbt ataonle dev hafa)
            📌 Nom :
            run_dbt_models

            🎯 Fonctionnalités :
            exécuter transformations SQL
            créer tables analytics

            📤 Output :
            staging + fact + dim tables

        🟪 TASK 5 — Run dbt tests
            📌 Nom :
            run_dbt_tests

            🎯 Fonctionnalités :
            tests qualité dbt
            not null
            unique
            relations

        🟥 TASK 6 — Update aggregations (optionnel)
            📌 Nom :
            update_aggregations

            🎯 Fonctionnalités :
            recalcul KPI :
            moyenne 7 jours
            moyenne 30 jours
            optimisation analytics

        📢 TASK 8 — Send notifications (bonus)
            📌 Nom :
            send_notifications

            🎯 Fonctionnalités :
            envoyer email
            webhook Slack / Telegram
            logs alertes

        ORDRE D EXECUTION DU DAG :
            extract_weather_data
                    ↓
            load_raw_weather
                    ↓
            validate_raw_data
                    ↓
            run_dbt_models
                    ↓
            run_dbt_tests
                    ↓
            update_aggregations
                    ↓
            generate_alerts
                    ↓
            send_notifications

        TRIGGER AIRFLOW :
            0 */3 * * *
            toutes les 3h
