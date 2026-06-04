👤 1. TOI — Data Engineer (Airflow + dbt + PostgreSQL)
🎯 Objectif

Construire tout le pipeline de données fiable

🔧 Fonctionnalités à implémenter
1. Ingestion des données (Airflow)

Fonctionnalités :

Planification toutes les 3h
Appel API météo
Gestion des erreurs API (timeout, réponse vide)
Retry automatique
Logging des exécutions

Concrètement tu fais :

DAG weather_ingestion_dag.py
Task :
extract_weather_data
transform_to_json
load_to_postgres

Bonus pro :

Historique des runs (succès / échec)
2. Stockage brut (PostgreSQL)

Fonctionnalités :

Table raw_weather
Insertion des données sans transformation
Gestion des doublons

Champs typiques :

city
datetime
temperature
humidity
wind_speed
raw_json
3. Transformation (dbt)

Fonctionnalités :

a. Staging
Nettoyage des données
Formatage des dates
Suppression des valeurs nulles
b. Data Warehouse (analytics)
fact_weather
dim_city
dim_date
c. Calculs métier
Moyenne température 7j / 30j
Score de confort (temp + humidité)
Détection d’alertes :
chaleur (> 35°C)
froid (< 10°C)
pluie forte
4. Data Quality (🔥 important)

Fonctionnalités :

Vérifier :
pas de valeurs nulles critiques
température réaliste
Tests dbt :
unique
not null
📦 Livrables attendus
DAG Airflow fonctionnel
Base PostgreSQL structurée
Projet dbt complet
Données propres dans analytics
👩‍💻 2. Backend Developer (FastAPI)
🎯 Objectif

Exposer les données via API propre

🔧 Fonctionnalités
1. Connexion base de données
Connexion PostgreSQL
Gestion pool de connexions
2. API Endpoints
/weather/today
météo actuelle par ville
/weather/history
historique météo (filtre date)
/weather/alerts
retourne alertes actives
/analytics/trends
tendances 7j / 30j
/cities
liste des villes disponibles
3. Filtrage & paramètres
ville
date
plage de dates
4. Documentation automatique
Swagger UI intégré
5. Gestion erreurs
ville inexistante
données absentes
📦 Livrables
API FastAPI fonctionnelle
Documentation Swagger
JSON propre et structuré
🎨 3. Frontend Developer (React ou Streamlit)
🎯 Objectif

Créer un dashboard interactif

🔧 Fonctionnalités
1. Interface utilisateur
Sélection ville
Sélection date
2. Graphiques
Température (line chart)
Précipitations
Humidité
3. Carte (optionnel mais 🔥)
Affichage des villes
Couleur selon température
4. Appels API
Consommer FastAPI
Mise à jour dynamique
5. Affichage alertes
badges :
🔴 chaleur
🔵 froid
📦 Livrables
Dashboard fonctionnel
UI propre
Connexion API OK
📊 4. Data Analyst (Power BI)
🎯 Objectif

Créer des dashboards décisionnels

🔧 Fonctionnalités
1. Connexion aux données
PostgreSQL ou export CSV
2. KPI (très important)
Température moyenne
Nombre d’alertes
Ville la plus chaude
3. Visualisations
Bar chart → températures par ville
Line chart → évolution temps
Heatmap → intensité météo
4. Filtres
ville
date
5. Storytelling
tendances météo
anomalies
📦 Livrables
Dashboard Power BI
KPI clairs
Visualisations lisibles



weather_pipeline/
│
├── dags/
│   └── weather_dag.py
│
├── scripts/
│   ├── extract.py
│   ├── load.py
│   └── utils.py
│
├── config/
│   └── config.yaml
│
├── logs/              (généré automatiquement)
│
├── plugins/           (optionnel)
│
├── requirements.txt
│
└── docker-compose.yml (optionnel mais 🔥 recommandé)

📁 dags/ (🔥 obligatoire)

👉 C’est LE dossier principal

Contient :

tes DAGs Airflow
Exemple :
dags/
└── weather_dag.py

👉 Ce fichier :

définit les tâches
définit l’ordre
définit le scheduling
📁 scripts/ (🔥 très important)

👉 Là où tu mets la vraie logique

Contient :

🔹 extract.py
appel API météo
🔹 load.py
insertion PostgreSQL
🔹 utils.py
fonctions communes (format date, logs…)

👉 Avantage :

code propre
réutilisable
maintenable
📁 config/

👉 Pour éviter de hardcoder

Contient :

URL API
clés API
paramètres
Exemple :
api_url: "https://api.open-meteo.com/..."
cities:
  - Antananarivo
  - Mahajanga
📁 logs/

👉 Généré automatiquement par Airflow

Contient :

logs des DAGs
erreurs

👉 très utile pour debug

📁 plugins/ (optionnel)

👉 pour :

operators personnalisés
hooks

👉 pas obligatoire pour ton projet

📄 requirements.txt

👉 liste des dépendances :

apache-airflow
requests
psycopg2
pandas
🐳 docker-compose.yml (🔥 recommandé)

👉 pour lancer Airflow facilement

Contient :

Airflow
PostgreSQL
scheduler

👉 très utilisé en pro

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from scripts.extract import extract_data
from scripts.load import load_data

with DAG(
    dag_id="weather_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="0 */3 * * *",
    catchup=False
) as dag:

    extract_task = PythonOperator(
        task_id="extract",
        python_callable=extract_data
    )

    load_task = PythonOperator(
        task_id="load",
        python_callable=load_data
    )

    extract_task >> load_task

    dbt_project/
│
├── models/
│   ├── staging/
│   │   └── stg_weather.sql
│   │
│   ├── marts/
│   │   ├── fact_weather.sql
│   │   └── dim_city.sql
│   │
│   └── analytics/
│       └── weather_metrics.sql
│
├── tests/
│
├── dbt_project.yml
├── profiles.yml
└── packages.yml