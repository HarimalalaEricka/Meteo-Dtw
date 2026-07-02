automatisation -> declencheur
visualisation
AirFlow et DBT
ETL

asina declencheur isakin ny etape dia afaka tapahana refa tsy mety fa tsy refa tonga ary voa tsy mety nefa declencheur tsy misy


docker exec -it weather_postgres psql -U airflow -d weather_db -c "\dt"
docker exec -it weather_postgres psql -U airflow -d weather_db


1. Données brutes — raw_weather
C'est là qu'Airflow insère directement ce qu'il récupère de l'API open-meteo, sans transformation. Table dans le schéma public.
2. Données nettoyées — stg_weather (vue dbt)
Vue créée par dbt qui filtre/valide les données de raw_weather (types corrects, valeurs dans des plages réalistes).
3. Données finales pour l'analyse — les tables "marts"

dim_city → dimension des villes (5 lignes, vu ton dernier dbt run)
dim_date → dimension calendaire (1096 lignes = ~3 ans de dates)
fact_weather → table de faits, agrégations journalières par ville
weather_alerts → alertes météo calculées
weather_metrics → moyennes glissantes 7j/30j + score de confort climatique