"""
weather_model.py
Requêtes SQL centralisées (pas d'ORM, requêtes brutes vers les tables dbt)
"""

SQL_GET_CITIES = """
    SELECT DISTINCT *
    FROM dim_city
    ORDER BY city_name;
"""

SQL_WEATHER_TODAY = """
    SELECT
        city,
        date_key,
        avg_temperature_c AS temperature_c,
        avg_humidity_pct AS humidity_pct,
        avg_wind_speed_kph AS wind_speed_kph,
        total_precipitation_mm AS precipitation_mm
    FROM fact_weather
    WHERE date_key = CURRENT_DATE
    {city_filter}
    ORDER BY city;
"""

SQL_WEATHER_HISTORY = """
    SELECT
        city,
        date_key,
        avg_temperature_c,
        avg_humidity_pct,
        avg_wind_speed_kph,
        total_precipitation_mm
    FROM fact_weather
    WHERE 1=1
    {city_filter}
    {date_from_filter}
    {date_to_filter}
    ORDER BY date_key DESC, city;
"""

SQL_TRENDS = """
    SELECT
        city,
        date_key,
        avg_temperature_c,
        avg_temp_7d,
        avg_temp_30d,
        total_precip_7d,
        total_precip_30d,
        comfort_level
    FROM weather_metrics
    WHERE 1=1
    {city_filter}
    ORDER BY date_key DESC, city;
"""

SQL_SUMMARY_HOTTEST = """
    SELECT
        city,
        avg_temperature_c
    FROM fact_weather
    WHERE date_key = CURRENT_DATE
    ORDER BY avg_temperature_c DESC
    LIMIT 1;
"""

SQL_SUMMARY_COLDEST = """
    SELECT
        city,
        avg_temperature_c
    FROM fact_weather
    WHERE date_key = CURRENT_DATE
    ORDER BY avg_temperature_c ASC
    LIMIT 1;
"""

SQL_SUMMARY_AVG = """
    SELECT
        AVG(avg_temperature_c) AS avg_temperature_global
    FROM fact_weather
    WHERE date_key = CURRENT_DATE;
"""

SQL_ALERTS = """
    SELECT
        city,
        date_key AS alert_date,
        alert_type,
        alert_severity AS severity,
        max_temperature_c,
        min_temperature_c,
        total_precipitation_mm,
        is_alert
    FROM weather_alerts
    WHERE 1=1
    {city_filter}
    ORDER BY date_key DESC;
"""