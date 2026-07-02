"""
analytics_service.py
Logique métier pour les endpoints /analytics
"""
from database.connection import execute_query
from models.weather_model import (
    SQL_TRENDS, SQL_SUMMARY_HOTTEST, SQL_SUMMARY_COLDEST, SQL_SUMMARY_AVG
)


def get_trends(city: str = None) -> list[dict]:
    city_filter = "AND city = %s" if city else ""
    query = SQL_TRENDS.format(city_filter=city_filter)
    params = (city,) if city else None
    return execute_query(query, params)


def get_summary() -> dict:
    hottest = execute_query(SQL_SUMMARY_HOTTEST)
    coldest = execute_query(SQL_SUMMARY_COLDEST)
    avg_temp = execute_query(SQL_SUMMARY_AVG)

    return {
        "hottest_city": hottest[0]["city"] if hottest else None,
        "hottest_temp": hottest[0]["avg_temperature_c"] if hottest else None,
        "coldest_city": coldest[0]["city"] if coldest else None,
        "coldest_temp": coldest[0]["avg_temperature_c"] if coldest else None,
        "avg_temperature_global": avg_temp[0]["avg_temperature_global"] if avg_temp else None,
    }