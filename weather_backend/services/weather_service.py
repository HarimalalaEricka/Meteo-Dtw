"""
weather_service.py
Logique métier pour les endpoints /weather
"""
from database.connection import execute_query
from models.weather_model import SQL_GET_CITIES, SQL_WEATHER_TODAY, SQL_WEATHER_HISTORY


def get_all_cities() -> list[dict]:
    return execute_query(SQL_GET_CITIES)


def is_valid_city(city: str) -> bool:
    cities = [row["city_name"].lower() for row in get_all_cities()]
    return city.lower() in cities


def get_weather_today(city: str = None) -> list[dict]:
    city_filter = "AND city = %s" if city else ""
    query = SQL_WEATHER_TODAY.format(city_filter=city_filter)
    params = (city,) if city else None
    return execute_query(query, params)


def get_weather_history(city: str = None, date_from: str = None, date_to: str = None) -> list[dict]:
    city_filter = "AND city = %s" if city else ""
    date_from_filter = "AND date_key >= %s" if date_from else ""
    date_to_filter = "AND date_key <= %s" if date_to else ""

    query = SQL_WEATHER_HISTORY.format(
        city_filter=city_filter,
        date_from_filter=date_from_filter,
        date_to_filter=date_to_filter,
    )

    params = tuple(p for p in [city, date_from, date_to] if p is not None)
    return execute_query(query, params)