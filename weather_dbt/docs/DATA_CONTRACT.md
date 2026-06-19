# Data Contract: raw_weather

## Vue d'ensemble
**Table source** : `raw_weather`  
**Schéma** : `public`  
**Source** : Apache Airflow (task: `extract_weather_data`, `load_raw_weather`)  
**Fréquence** : Toutes les 3 heures  
**Rétention** : Non définie (suggestion: 6 mois minimum)

---

## Colonnes

| Colonne | Type SQL | Nullable | Description | Validations |
|---------|----------|----------|-------------|-------------|
| `id` | SERIAL PRIMARY KEY | Non | Identifiant unique | >= 1 |
| `city` | VARCHAR(100) | Non | Nom de la ville | Max 100 caractères |
| `datetime` | TIMESTAMP | Non | Timestamp de l'observation | Format ISO8601 |
| `temperature` | FLOAT | Oui | Température en Celsius | Entre -90 et 60 |
| `humidity` | FLOAT | Oui | Humidité en % | Entre 0 et 100 |
| `wind_speed` | FLOAT | Oui | Vitesse du vent en km/h | >= 0 |
| `precipitation` | FLOAT | Oui | Précipitation en mm | >= 0 |
| `weather_code` | INTEGER | Oui | Code WMO | [Voir WMO Codes] |
| `raw_json` | TEXT | Oui | JSON brut de l'API | Format JSON valide |
| `ingested_at` | TIMESTAMP | Non (DEFAULT) | Timestamp d'insertion | AUTO: NOW() |

---

## Contraintes

- **UNIQUE** : `(city, datetime)` — Pas de doublons par ville/heure
- **PRIMARY KEY** : `id`

---

## Villes supportées

1. Antananarivo (lat: -18.9137, lon: 47.5361)
2. Mahajanga (lat: -15.7162, lon: 46.3190)
3. Toamasina (lat: -18.1492, lon: 49.4023)
4. Fianarantsoa (lat: -21.4545, lon: 47.0868)
5. Toliara (lat: -23.3568, lon: 43.6667)

---

## Exemple d'enregistrement

```sql
INSERT INTO raw_weather (city, datetime, temperature, humidity, wind_speed, precipitation, weather_code, raw_json)
VALUES (
  'Antananarivo',
  '2024-06-19 10:00:00',
  22.5,
  65.0,
  8.2,
  0.0,
  1,
  '{"temperature_2m": 22.5, "relativehumidity_2m": 65, "windspeed_10m": 8.2, "precipitation": 0, "weathercode": 1}'
);
```

---

## Tests dbt attendus

- `not_null` : `id`, `city`, `datetime`
- `unique` : `id`, `(city, datetime)`
- Valeurs entre plages : `temperature`, `humidity`, `wind_speed`, `precipitation`

---

## Notes d'intégration

- **Airflow** crée et alimente cette table via `load.py`
- **dbt** la consomme dans `stg_weather` pour transformation
- **Backend API** consomme les tables analytiques (pas directement `raw_weather`)
- En cas de redéploiement, la table est recréée via `CREATE TABLE IF NOT EXISTS`

---

## Historique des modifications

| Date | Modification | Auteur |
|------|--------------|--------|
| 2024-06-19 | Initial | dbt team |
