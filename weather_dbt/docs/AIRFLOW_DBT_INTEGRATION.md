# Intégration Airflow ↔ dbt

## Vue d'ensemble

Le pipeline météo est orchestré par Airflow, qui alimente dbt avec des données brutes.

```
Airflow (extract → load)
    ↓
raw_weather (PostgreSQL)
    ↓
dbt (transform)
    ↓
Analytics tables (fact_weather, dim_city, dim_date, weather_metrics, weather_alerts)
    ↓
Backend API / Power BI
```

---

## Flux détaillé

### 1️⃣ Airflow : Extraction et Chargement (Toutes les 3h)

**Task: `extract_weather_data`**
- Appelle l'API open-meteo pour 5 villes
- Récupère: `temperature`, `humidity`, `wind_speed`, `precipitation`, `weather_code`
- Fournit: Données brutes en mémoire (XCom)

**Task: `load_raw_weather`**
- Crée la table `raw_weather` si inexistante
- Insère les données avec gestion des doublons (UNIQUE constraint)
- **Output** : Données dans `public.raw_weather`

**Colonnes insérées:**
```
id | city | datetime | temperature | humidity | wind_speed | precipitation | weather_code | raw_json | ingested_at
```

---

### 2️⃣ dbt : Transformation

**Source (raw_weather)**
```yaml
sources:
  - name: weather
    tables:
      - name: raw_weather
```

**Pipeline de modèles dbt**

```
raw_weather
    ↓
stg_weather (vue - nettoyage et validation)
    ↓
┌─────────────────────────────────────┐
├─ fact_weather (table - agrégation)  │
├─ dim_city (table - villes)          │
├─ dim_date (table - calendrier)      │
│   ↓
├─ weather_metrics (table - KPI 7j/30j, score confort)
├─ weather_alerts (table - alertes canicule/froid/pluie)
└─────────────────────────────────────┘
```

**Modèles créés**

| Modèle | Type | Description |
|--------|------|-------------|
| `stg_weather` | VUE | Données nettoyées et validées |
| `fact_weather` | TABLE | Agrégation quotidienne par ville |
| `dim_city` | TABLE | Référence des villes |
| `dim_date` | TABLE | Calendrier + attributs temporels |
| `weather_metrics` | TABLE | KPI: moyennes 7j/30j, score confort |
| `weather_alerts` | TABLE | Alertes météo (seuils: >35°C, <10°C, >20mm) |

---

## Configuration PostgreSQL

### Schémas utilisés

| Schéma | Propriétaire | Tables |
|--------|--------------|--------|
| `public` | Airflow | `raw_weather` |
| `weather_analytics` | dbt | `stg_weather`, `fact_weather`, `dim_*`, `weather_*` |

### Paramètres dbt (profiles.yml)

```yaml
weather_dbt:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      user: postgres
      password: postgres
      port: 5432
      dbname: meteo_dwh
      schema: weather_analytics
      threads: 4
```

---

## Exécution dbt

### 1. Lancer les modèles

```bash
cd weather_dbt
dbt run
```

Ordre d'exécution :
1. `stg_weather` (dépend de `raw_weather`)
2. `dim_city`, `dim_date` (en parallèle)
3. `fact_weather` (dépend de `stg_weather`)
4. `weather_metrics`, `weather_alerts` (dépendent de `fact_weather`)

### 2. Charger les données de référence (seeds)

```bash
dbt seed
```

Charge:
- `seed_cities.csv` → `seed_cities` table
- `seed_raw_weather_sample.csv` → données de test

### 3. Valider la qualité

```bash
dbt test
```

Vérifie:
- `not_null` sur colonnes critiques
- `unique` sur identifiants
- Valeurs dans les plages attendues

### 4. Générer la documentation

```bash
dbt docs generate
dbt docs serve
```

---

## Seuils d'alertes

Définis dans `macros/alerts_logic.sql` et configuration Airflow :

| Type | Seuil | Gravité |
|------|-------|---------|
| Canicule | temp > 35°C | WARNING / CRITICAL si > 40°C |
| Froid | temp < 10°C | WARNING / CRITICAL si < 0°C |
| Pluie forte | precip > 20mm | WARNING / CRITICAL si > 40mm |

---

## Points d'intégration côté Backend

**Tables à consommer:**
- `weather_analytics.fact_weather` — données consolidées par jour
- `weather_analytics.dim_city` — référence des villes
- `weather_analytics.weather_metrics` — KPI et tendances
- `weather_analytics.weather_alerts` — alertes actives

**Endpoints API suggérés:**
- `GET /weather/today` → `fact_weather` (jour courant)
- `GET /analytics/trends` → `weather_metrics` (7j/30j)
- `GET /weather/alerts` → `weather_alerts` (actives)

---

## Troubleshooting

### Erreur: "source 'weather.raw_weather' not found"
- Vérifier que `raw_weather` existe dans `public` schema
- Vérifier les permissions PostgreSQL pour l'utilisateur dbt

### Erreur: "UNIQUE constraint violation"
- Airflow essaie d'insérer des doublons (city, datetime)
- Exécuter : `DELETE FROM raw_weather WHERE city = '...' AND datetime = ...;`

### dbt ne crée pas les tables
- Vérifier que le schéma `weather_analytics` existe
- Vérifier les permissions de dbt sur le schéma
- Exécuter: `dbt run --debug`

---

## Prochaines étapes

1. ✅ Lancer Airflow (extraction toutes les 3h)
2. ✅ Exécuter `dbt seed` + `dbt run`
3. ✅ Valider avec `dbt test`
4. ✅ Intégrer avec Backend API
5. ✅ Connecter Power BI

---

## Contacts & Responsabilités

| Rôle | Responsable | Tâche |
|------|-------------|-------|
| **Airflow Dev** | [Nom] | Orchestration, extraction API, chargement raw_weather |
| **dbt Dev** | [Vous] | Transformation, modélisation, tests qualité |
| **Backend Dev** | [Nom] | API REST, consommation tables analytics |
| **Power BI Dev** | [Nom] | Dashboards, visualisations, rapports |
