"""
alerts.py
Endpoints /weather/alerts
"""
from fastapi import APIRouter, Query
from services import alert_service, weather_service
from schemas.weather_schema import AlertOut
from utils.helpers import ensure_city_exists, handle_db_error

router = APIRouter()


@router.get("/weather/alerts", response_model=list[AlertOut])
def alerts(city: str = Query(None)):
    try:
        ensure_city_exists(city, weather_service.is_valid_city)
        return alert_service.get_alerts(city)
    except ConnectionError as e:
        handle_db_error(e)