BACKEND API
    ROLE : Le backend est la couche d’exposition des données
        Il sert à :
            lire les données transformées par dbt
            fournir une API REST
            filtrer et structurer les données
            envoyer des réponses JSON au frontend / Power BI

    STRUCTURE DU DOSSIER : 
        backend/
        │
        ├── main.py
        │
        ├── database/
        │   └── connection.py
        │
        ├── models/
        │   └── weather_model.py
        │
        ├── routes/
        │   ├── weather.py
        │   ├── analytics.py
        │   └── alerts.py
        │
        ├── services/
        │   ├── weather_service.py
        │   ├── analytics_service.py
        │   └── alert_service.py
        │
        ├── schemas/
        │   └── weather_schema.py
        │
        ├── utils/
        │   └── helpers.py
        │
        └── requirements.txt

    FONCTIONNALITÉS GLOBALES :
        ✔️ Exposer les données
            API REST (JSON)
        ✔️ Lire PostgreSQL (dbt tables)
            fact_weather
            dim_city
            weather_metrics
            alerts
        ✔️ Filtrer les données
            par ville
            par date
            par période
        ✔️ Transformer les résultats
            SQL → JSON structuré
        ✔️ Gérer les erreurs
            ville inexistante
            données absentes
        ✔️ Fournir documentation API
            Swagger UI

    ENDPOINTS PRINCIPAUX : 
        🌤️ WEATHER API
            📌 GET /weather/today
            🎯 Fonctionnalités :
                météo actuelle par ville

            📌 GET /weather/history
            🎯 Fonctionnalités :
                historique météo
                filtrage par ville + date

            📌 GET /cities
            🎯 Fonctionnalités :
                liste des villes disponibles

        📊 ANALYTICS API
            📌 GET /analytics/trends
            🎯 Fonctionnalités :
                moyenne température 7 jours
                moyenne 30 jours
                évolution météo

            📌 GET /analytics/summary
            🎯 Fonctionnalités :
                ville la plus chaude
                ville la plus froide
                statistiques globales

        🚨 ALERTS API
            📌 GET /weather/alerts
            🎯 Fonctionnalités :
                récupérer alertes générées par Airflow
                affichage des événements extrêmes
                📌 Types d’alertes :
                    🔴 canicule (> 35°C)
                    🔵 froid (< 10°C)
                    🌧️ pluie forte

    FLUX DU BACKEND : 
        PostgreSQL (dbt analytics)
                ↓
            FastAPI
                ↓
        JSON REST API
                ↓
        Frontend / Power BI