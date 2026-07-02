{{
  config(
    materialized='table'
  )
}}

with daily_data as (
    select
        date_key,
        city,
        max_temperature_c,
        min_temperature_c,
        total_precipitation_mm
    from {{ ref('fact_weather') }}
),

-- Appliquer la macro d'alerte pour chaque ligne
alerts as (
    select
        date_key,
        city,
        max_temperature_c,
        min_temperature_c,
        total_precipitation_mm,
        {{ generate_weather_alert(
            'max_temperature_c',
            'min_temperature_c',
            'total_precipitation_mm'
        ) }} as alert_type,
        {{ get_alert_severity(
            'max_temperature_c',
            'min_temperature_c',
            'total_precipitation_mm'
        ) }} as alert_severity
    from daily_data
)

select
    date_key,
    city,
    max_temperature_c,
    min_temperature_c,
    total_precipitation_mm,
    alert_type,
    alert_severity,
    case
        when alert_type != 'None' then true
        else false
    end as is_alert
from alerts
where alert_type != 'None'
order by date_key desc, alert_severity desc
