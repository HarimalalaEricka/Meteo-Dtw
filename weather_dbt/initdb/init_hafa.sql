CREATE DATABASE meteo_dwh;
\c meteo_dwh
CREATE SCHEMA IF NOT EXISTS weather_analytics;

CREATE TABLE raw_weather (
  id uuid primary key,
  city text,
  country text,
  country_code text,
  timezone text,
  latitude numeric(10,6),
  longitude numeric(10,6),
  observation_time timestamp,
  temperature_c numeric,
  humidity_pct numeric,
  wind_speed_kph numeric,
  precipitation_mm numeric,
  pressure_hpa numeric,
  cloud_cover_pct numeric,
  uv_index numeric
);