{{
  config(
    materialized='table'
  )
}}

with daily_data as (
    select
        date_key,
        city,
        avg_temperature_c,
        avg_humidity_pct,
        avg_wind_speed_kph,
        total_precipitation_mm
    from {{ ref('fact_weather') }}
),

-- Calculs sur 7 jours
rolling_7d as (
    select
        date_key,
        city,
        avg_temperature_c,
        avg(avg_temperature_c) over (
            partition by city
            order by date_key
            rows between 6 preceding and current row
        ) as avg_temp_7d,
        sum(total_precipitation_mm) over (
            partition by city
            order by date_key
            rows between 6 preceding and current row
        ) as total_precip_7d
    from daily_data
),

-- Calculs sur 30 jours
rolling_30d as (
    select
        date_key,
        city,
        avg_temperature_c,
        avg_temp_7d,
        total_precip_7d,
        avg(avg_temperature_c) over (
            partition by city
            order by date_key
            rows between 29 preceding and current row
        ) as avg_temp_30d,
        sum(total_precipitation_mm) over (
            partition by city
            order by date_key
            rows between 29 preceding and current row
        ) as total_precip_30d
    from rolling_7d
),

-- Calcul du score de confort climatique
comfort_score as (
    select
        date_key,
        city,
        avg_temperature_c,
        avg_temp_7d,
        avg_temp_30d,
        total_precip_7d,
        total_precip_30d,
        case
            when avg_temperature_c between 18 and 24 then 'Excellent'
            when avg_temperature_c between 15 and 27 then 'Good'
            when avg_temperature_c between 10 and 30 then 'Moderate'
            else 'Uncomfortable'
        end as comfort_level
    from rolling_30d
)

select
    date_key,
    city,
    avg_temperature_c,
    avg_temp_7d,
    avg_temp_30d,
    total_precip_7d,
    total_precip_30d,
    comfort_level
from comfort_score
order by date_key desc, city;
