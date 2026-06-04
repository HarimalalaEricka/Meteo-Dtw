POWER BI
    ROLE : Power BI est la couche de visualisation et décision
        Il sert à :
            transformer les données en dashboards
            analyser les tendances météo
            suivre les KPI
            aider à la prise de décision

    SOURCE DES DONNÉES : 
        PostgreSQL (tables dbt : analytics)

    FONCTIONNALITÉS GLOBALES : 
        ✔️ Visualisation des données
            graphiques météo
            cartes géographiques
            courbes de température
        ✔️ Analyse KPI
            température moyenne
            humidité moyenne
            nombre d’alertes
        ✔️ Comparaison
            villes entre elles
            périodes (7j vs 30j)
        ✔️ Monitoring météo
            évolution temps réel (refresh)
            anomalies climatiques
        ✔️ Reporting
            rapports PDF / dashboard partagé

    DASHBOARDS PRINCIPAUX :
        🟦 4.1 Dashboard global météo
            🎯 Contenu :
                température moyenne globale
                carte des villes
                météo actuelle

        🟩 4.2 Dashboard KPI
            🎯 Contenu :
                moyenne température 7 jours
                moyenne 30 jours
                humidité moyenne
                vitesse du vent

        🟥 4.3 Dashboard alertes
            🎯 Contenu :
                nombre d’alertes
                types d’alertes :
                    canicule 🔴
                    froid 🔵
                    pluie 🌧️
                    gravité

        🟨 4.4 Comparaison des villes
            🎯 Contenu :
                Antananarivo vs autres villes
                classement température
                ranking climat

        
    VISUALISATIONS UTILISÉES : 
        📊 Graphiques :
            Line chart → température
            Bar chart → comparaison villes
            Area chart → évolution météo
        🌍 Carte :
            carte géographique des villes
            heatmap température
        🚨 KPI Cards :
            température moyenne
            nombre d’alertes
            ville la plus chaude

    FLUX POWER BI : 
        PostgreSQL (dbt analytics)
                ↓
            Power BI
                ↓
        Dashboards & rapports