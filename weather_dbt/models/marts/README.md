# Marts Layer

Marts contain fact tables and dimension tables ready for analytics.

**Fact Tables:**
- `fact_weather.sql`: Main weather metrics aggregated by day
Agrège météo quotidienne par ville
Calcule moyenne/min/max température, humidité, vent, précipitation totale

- `schema.yml`
Décrit fact_weather
Ajoute des tests not_null

**Dimension Tables:**
- `dim_city.sql`: City reference data
- `dim_date.sql`: Date reference data

**Purpose:**
- Provide structured data for analysis
- Enable star schema queries
- Support frontend and Power BI dashboards
