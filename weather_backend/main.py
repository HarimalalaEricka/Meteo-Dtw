"""
main.py
Point d'entrée FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import weather, analytics, alerts

app = FastAPI(
    title="Weather Data Warehouse API",
    description="API exposant les données météo transformées par dbt (fact_weather, weather_metrics, weather_alerts)",
    version="1.0.0",
)

# CORS — à restreindre plus tard si un frontend précis est déployé
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(weather.router, tags=["Weather"])
app.include_router(analytics.router, tags=["Analytics"])
app.include_router(alerts.router, tags=["Alerts"])


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "weather-backend-api"}