"""
alert_service.py
Logique métier pour les endpoints /alerts
"""
from database.connection import execute_query
from models.weather_model import SQL_ALERTS


def get_alerts(city: str = None) -> list[dict]:
    city_filter = "AND city = %s" if city else ""
    query = SQL_ALERTS.format(city_filter=city_filter)
    params = (city,) if city else None
    return execute_query(query, params)