
DBT
    ROLE : dbt est la couche de transformation SQL du pipeline
        Il sert a :
            nettoyer les données brutes (raw)
            structurer les données (staging)
            créer des modèles analytiques (fact & dim)
            calculer les KPI météo
            tester la qualité des données

    STRUCTURE DU DOSSIER DBT :
        dbt_project/
        │
        ├── models/
        │   ├── staging/
        │   │   └── stg_weather.sql
        │   │
        │   ├── marts/
        │   │   ├── fact_weather.sql
        │   │   ├── dim_city.sql
        │   │   └── dim_date.sql
        │   │
        │   └── analytics/
        │       └── weather_metrics.sql
        │
        ├── tests/
        │   ├── test_not_null.yml
        │   ├── test_unique.yml
        │
        ├── macros/
        │   └── alerts_logic.sql
        │
        ├── seeds/
        │   └── cities.csv
        │
        ├── snapshots/
        │
        ├── dbt_project.yml
        └── profiles.yml

    FONCTIONNALITÉS GLOBALES :
        ✔️ Nettoyage des données
            suppression nulls
            formatage dates
            normalisation champs
        ✔️ Structuration data warehouse
            staging layer
            fact tables
            dimension tables
        ✔️ Calculs métier
            moyenne température
            alertes météo (logique SQL)
            KPI 7j / 30j
        ✔️ Tests qualité
            not null
            unique
            relations valides
        ✔️ Documentation automatique
            lineage des données
            description tables

    MODELS DBT : 
        🟦 4.1 STAGING LAYER
            📌 Fichier :
            stg_weather.sql

            🎯 Fonctionnalités :
            nettoyage données brutes
            conversion types
            suppression erreurs

            📥 Source :
            raw_weather

        🟩 4.2 FACT TABLE (analyse principale)
            📌 Fichier :
            fact_weather.sql

            🎯 Fonctionnalités :
            données météo agrégées
            calculs journaliers
            Exemples :
            température moyenne
            humidité moyenne
            vitesse vent

        🟨 4.3 DIMENSION TABLES
            📌 Fichiers :
            dim_city.sql
            dim_date.sql

            🎯 Fonctionnalités :
            structure des dimensions
            support des analyses

        🟧 4.4 ANALYTICS LAYER
            📌 Fichier :
            weather_metrics.sql

            🎯 Fonctionnalités :
            KPI avancés
            tendances météo
            indicateurs globaux
            Exemples :
            moyenne 7 jours
            moyenne 30 jours
            score confort climatique


        🧪 5. TESTS DBT
            ✔️ Test NOT NULL
            pas de valeurs manquantes critiques
            ✔️ Test UNIQUE
            pas de doublons (city + date)
            ✔️ Test RELATIONSHIP
            clés étrangères valides

        🧠 6. MACROS DBT
            👉 fonctions SQL réutilisables
            🎯 Exemples :
                calcul score météo
                logique d’alerte

        🌱 7. SEEDS
            👉 données statiques

            Exemple :
            liste des villes
            zones climatiques

        📸 8. SNAPSHOTS
            👉 historique des données dans le temps

            Utilisation :
            suivre évolution météo
            comparer périodes
        
        ⚙️ 9. EXECUTION DBT
            Commandes :
                dbt run
                👉 exécute les modèles SQL

                dbt test
                👉 vérifie la qualité des données

                dbt docs generate
                👉 génère documentation
    
    FLUX DBT : 
        raw_weather (PostgreSQL)
                ↓
        staging (clean data)
                ↓
        marts (fact + dim)
                ↓
        analytics (KPI)