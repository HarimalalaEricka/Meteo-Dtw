# Weather dbt Project

Transformation layer for the Meteo-DTW pipeline.

## Installation

1. Install dbt: `pip install dbt-postgres`
2. Update `profiles.yml` with your PostgreSQL credentials
3. Run `dbt debug` to verify connection

## Running

```bash
# Run all models
dbt run

# Run specific model
dbt run --select stg_weather

# Run tests
dbt test

# Generate documentation
dbt docs generate
dbt docs serve

# Create seeds
dbt seed

# Take snapshots
dbt snapshot
```

## Project Structure

- `models/staging/` → Data cleaning layer
- `models/marts/` → Fact & dimension tables
- `models/analytics/` → KPI and metric calculations
- `tests/` → Data quality tests
- `macros/` → Reusable SQL functions
- `seeds/` → Static reference data
- `snapshots/` → Historical dimension tracking

## Documentation

See README.md files in each subdirectory for details.
