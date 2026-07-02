"""
analytics.py
Endpoints /analytics
"""
from fastapi import APIRouter, Query
from services import analytics_service, weather_service
from schemas.weather_schema import TrendOut, SummaryOut
from utils.helpers import ensure_city_exists, handle_db_error

router = APIRouter()


@router.get("/analytics/trends", response_model=list[TrendOut])
def trends(city: str = Query(None)):
    try:
        ensure_city_exists(city, weather_service.is_valid_city)
        return analytics_service.get_trends(city)
    except ConnectionError as e:
        handle_db_error(e)


@router.get("/analytics/summary", response_model=SummaryOut)
def summary():
    try:
        return analytics_service.get_summary()
    except ConnectionError as e:
        handle_db_error(e)