# ===========================================================
# start.ps1 - Demarrage environnement Airflow
# ===========================================================

Write-Host ""
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "   Demarrage environnement Airflow" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

# Aller dans le dossier projet
$projectPath = "E:\GitHub\Meteo-Dtw\weather_pipeline_airflow"
Write-Host "Dossier projet : $projectPath" -ForegroundColor Yellow
cd $projectPath

# Activer le venv Python
Write-Host "Activation du venv Python..." -ForegroundColor Yellow
.\airflow_env\Scripts\Activate.ps1

# Definir AIRFLOW_HOME
$env:AIRFLOW_HOME = "E:\GitHub\Meteo-Dtw\weather_pipeline_airflow\airflow_home"
Write-Host "AIRFLOW_HOME = $env:AIRFLOW_HOME" -ForegroundColor Yellow

Write-Host ""
Write-Host "===========================================" -ForegroundColor Green
Write-Host "   ENVIRONNEMENT PRET !" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Commandes disponibles :" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Terminal 1 (Webserver) :" -ForegroundColor White
Write-Host "     airflow webserver --port 8080" -ForegroundColor Gray
Write-Host ""
Write-Host "  Terminal 2 (Scheduler) :" -ForegroundColor White
Write-Host "     airflow scheduler" -ForegroundColor Gray
Write-Host ""
Write-Host "  Interface web :" -ForegroundColor White
Write-Host "     http://localhost:8080" -ForegroundColor Gray
Write-Host "     Login : admin / admin" -ForegroundColor Gray
Write-Host ""