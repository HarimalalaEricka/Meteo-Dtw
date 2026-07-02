"""
weather.py
Endpoints /weather et /cities
"""
from fastapi import APIRouter, Query, HTTPException
from services import weather_service
from schemas.weather_schema import CityOut, WeatherTodayOut, WeatherHistoryOut
from utils.helpers import ensure_city_exists, handle_db_error

router = APIRouter()


@router.get("/cities", response_model=list[CityOut])
def list_cities():
    try:
        return weather_service.get_all_cities()
    except ConnectionError as e:
        handle_db_error(e)


@router.get("/weather/today", response_model=list[WeatherTodayOut])
def weather_today(city: str = Query(None, description="Filtrer par ville")):
    try:
        ensure_city_exists(city, weather_service.is_valid_city)
        data = weather_service.get_weather_today(city)
        if not data:
            raise HTTPException(status_code=404, detail="Aucune donnée météo pour aujourd'hui")
        return data
    except ConnectionError as e:
        handle_db_error(e)


@router.get("/weather/history", response_model=list[WeatherHistoryOut])
def weather_history(
    city: str = Query(None),
    date_from: str = Query(None, description="Format YYYY-MM-DD"),
    date_to: str = Query(None, description="Format YYYY-MM-DD"),
):
    try:
        ensure_city_exists(city, weather_service.is_valid_city)
        return weather_service.get_weather_history(city, date_from, date_to)
    except ConnectionError as e:
        handle_db_error(e)