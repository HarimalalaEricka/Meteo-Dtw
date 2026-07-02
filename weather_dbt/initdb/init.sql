-- Init database, user and schema for weather_dbt
CREATE DATABASE meteo_dwh;

-- Create schema
\connect meteo_dwh;
CREATE SCHEMA IF NOT EXISTS weather_analytics;

-- Create a dedicated user
CREATE USER weather_user WITH PASSWORD 'weather_pass';
GRANT ALL PRIVILEGES ON DATABASE meteo_dwh TO weather_user;
GRANT USAGE ON SCHEMA weather_analytics TO weather_user;
GRANT CREATE ON SCHEMA weather_analytics TO weather_user;

-- You can add seed data or GRANTs for tables here
