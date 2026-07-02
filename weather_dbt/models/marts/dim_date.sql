{{
  config(
    materialized='table'
  )
}}

with date_range as (
    select
        generate_series(
            current_date - interval '2 years',
            current_date + interval '1 year',
            interval '1 day'
        )::date as date_key
)

select
    date_key,
    date_trunc('year', date_key)::date as year_start,
    date_trunc('month', date_key)::date as month_start,
    date_trunc('week', date_key)::date as week_start,
    extract(year from date_key)::integer as year,
    extract(month from date_key)::integer as month,
    extract(week from date_key)::integer as week,
    extract(day from date_key)::integer as day,
    extract(dow from date_key)::integer as day_of_week,
    to_char(date_key, 'Day') as day_name,
    to_char(date_key, 'Month') as month_name,
    case
        when extract(dow from date_key) in (0, 6) then true
        else false
    end as is_weekend
from date_range
order by date_key
