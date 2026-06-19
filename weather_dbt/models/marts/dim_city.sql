{{
  config(
    materialized='table'
  )
}}

with cities_data as (
    select *
    from {{ ref('seed_cities') }}
)

select
    city_id,
    city_name,
    latitude,
    longitude,
    country,
    region
from cities_data
