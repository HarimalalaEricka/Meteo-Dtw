{{
  config(
    materialized='view'
  )
}}

with raw as (
    select *
    from {{ source('weather', 'raw_weather') }}
),
cleaned as (
    select
        raw.id,
        nullif(trim(raw.city), '') as city,
        raw.datetime::timestamp as observation_at,
        date_trunc('hour', raw.datetime::timestamp) as observation_hour,
        date(raw.datetime::timestamp) as observation_date,
        raw.temperature::numeric as temperature_c,
        raw.humidity::numeric as humidity_pct,
        raw.wind_speed::numeric as wind_speed_kph,
        raw.precipitation::numeric as precipitation_mm,
        raw.weather_code::integer as weather_code,
        raw.raw_json::text as raw_json,
        raw.ingested_at::timestamp as ingested_at,
        -- Validation checks
        case
            when raw.temperature between -90 and 60 then raw.temperature::numeric
            else null
        end as valid_temperature_c,
        case
            when raw.humidity between 0 and 100 then raw.humidity::numeric
            else null
        end as valid_humidity_pct,
        case
            when raw.wind_speed >= 0 then raw.wind_speed::numeric
            else null
        end as valid_wind_speed_kph,
        case
            when raw.precipitation >= 0 then raw.precipitation::numeric
            else null
        end as valid_precipitation_mm
    from raw
)

select
    id,
    city,
    observation_at,
    observation_hour,
    observation_date,
    temperature_c,
    humidity_pct,
    wind_speed_kph,
    precipitation_mm,
    weather_code,
    raw_json,
    ingested_at,
    valid_temperature_c,
    valid_humidity_pct,
    valid_wind_speed_kph,
    valid_precipitation_mm
from cleaned
where city is not null
  and observation_at is not null
  and valid_temperature_c is not null
  and valid_humidity_pct is not null
  and valid_wind_speed_kph is not null
