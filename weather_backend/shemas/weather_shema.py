"""
weather_schema.py
Schémas Pydantic pour la validation et sérialisation des réponses
"""
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class CityOut(BaseModel):
    city: str


class WeatherTodayOut(BaseModel):
    city: str
    observation_date: date
    temperature_c: Optional[float] = None
    humidity_pct: Optional[float] = None
    wind_speed_kph: Optional[float] = None
    precipitation_mm: Optional[float] = None


class WeatherHistoryOut(BaseModel):
    city: str
    date_key: date
    avg_temperature_c: Optional[float] = None
    avg_humidity_pct: Optional[float] = None
    avg_wind_speed_kph: Optional[float] = None
    total_precipitation_mm: Optional[float] = None


class TrendOut(BaseModel):
    city: str
    date_key: date
    avg_temp_7d: Optional[float] = None
    avg_temp_30d: Optional[float] = None
    total_precip_7d: Optional[float] = None
    total_precip_30d: Optional[float] = None
    comfort_level: Optional[str] = None


class SummaryOut(BaseModel):
    hottest_city: Optional[str] = None
    hottest_temp: Optional[float] = None
    coldest_city: Optional[str] = None
    coldest_temp: Optional[float] = None
    avg_temperature_global: Optional[float] = None


class AlertOut(BaseModel):
    city: str
    alert_date: date
    alert_type: str
    severity: Optional[str] = None
    value: Optional[float] = None
    threshold: Optional[float] = None