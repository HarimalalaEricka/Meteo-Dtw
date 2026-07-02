# Tables pour l'analyse météo

## Source et préparation
- `raw_weather` : table source brute des données météo
- `stg_weather` : vue de nettoyage, validation et normalisation

## Tables métier
- `dim_city` : dimension des villes
- `dim_date` : dimension calendrier
- `fact_weather` : table de faits principale, agrégée par jour et par ville

## Tables d'analyse
- `weather_metrics` : indicateurs et KPIs météo
- `weather_alerts` : alertes météo générées à partir des mesures

## Tables à retenir en priorité
- `fact_weather`
- `dim_city`
- `dim_date`
- `weather_metrics`
- `weather_alerts`
