FRONTEND
    ROLE : Le frontend est la couche d’interaction utilisateur
        Il sert à :
            afficher les données météo
            consommer l’API FastAPI
            visualiser les KPI
            afficher les alertes
            rendre le projet interactif et lisible

    STRUCTURE DU DOSSIER : 
        Selon le choix de la technologie

    FONCTIONNALITÉS GLOBALES :
        ✔️ Affichage météo
            température actuelle
            humidité
            vent
        ✔️ Dashboards interactifs
            graphiques température
            évolution sur 7 / 30 jours
            comparaisons villes
        ✔️ Gestion des alertes
            affichage alertes météo
            badges couleur (rouge, bleu, etc.)
        ✔️ Cartographie (optionnel 🔥)
            carte des villes
            météo par région
        ✔️ Filtres utilisateur
            ville
            date
            période
        ✔️ Consommation API
            appel FastAPI
            affichage JSON transformé

    CONNEXION AU BACKEND :
        Frontend → HTTP Request → FastAPI → PostgreSQL

    ÉCRANS PRINCIPAUX : 
        🟦 Dashboard principal
            🎯 Contenu :
            météo actuelle
            résumé global
            alertes actives

        🟩 Page Analytics
            🎯 Contenu :
            graphiques température
            tendances 7j / 30j
            KPI météo

        🟥 Page Alerts
        🎯 Contenu :
        liste alertes
        type (canicule, froid)
        niveau de gravité

    VISUALISATIONS :
        📊 Graphiques :
            température (line chart)
            humidité
            précipitations
        📍 Carte :
            villes
            météo par zone
        🚨 Alertes :
            rouge = danger
            bleu = froid
            jaune = pluie

    FLUX FRONTEND :
        User
        ↓
        Frontend (React / Streamlit)
        ↓
        FastAPI (backend)
        ↓
        PostgreSQL (dbt analytics)
