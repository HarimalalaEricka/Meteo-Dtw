{{
  config(
    materialized='table'
  )
}}

select
  {{ ref('stg_weather') }}.observation_date as date_key,
  {{ ref('stg_weather') }}.city,
  avg({{ ref('stg_weather') }}.temperature_c) as avg_temperature_c,
  min({{ ref('stg_weather') }}.temperature_c) as min_temperature_c,
  max({{ ref('stg_weather') }}.temperature_c) as max_temperature_c,
  avg({{ ref('stg_weather') }}.humidity_pct) as avg_humidity_pct,
  min({{ ref('stg_weather') }}.humidity_pct) as min_humidity_pct,
  max({{ ref('stg_weather') }}.humidity_pct) as max_humidity_pct,
  avg({{ ref('stg_weather') }}.wind_speed_kph) as avg_wind_speed_kph,
  max({{ ref('stg_weather') }}.wind_speed_kph) as max_wind_speed_kph,
  sum({{ ref('stg_weather') }}.precipitation_mm) as total_precipitation_mm,
  count(*) as records_count,
  max({{ ref('stg_weather') }}.ingested_at) as last_updated
from {{ ref('stg_weather') }}
group by observation_date, city
order by observation_date desc, city
