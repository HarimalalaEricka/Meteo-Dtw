# Staging Layer

Staging models clean and normalize raw data from the source tables.

**Purpose:**
- Remove nulls and invalid data
- Convert data types
- Rename columns for consistency
- Create a reliable foundation for marts

**Models:**
- `stg_weather.sql`: Cleaned weather data from raw_weather
Nettoie les données de raw_weather
Normalise colonnes, types et valeurs invalides
Filtre les lignes sans city, observation_at, temperature_c, humidity_pct, wind_speed_kph

- `schema.yml` :
Déclare la source weather.raw_weather
Ajoute des tests not_null et unique pour stg_weather