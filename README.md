# OpenWeather End-to-End Data Pipeline

## Project Overview

This project implements an end-to-end data pipeline using a public REST API. Weather data is ingested from the OpenWeather API, stored in PostgreSQL, transformed using dbt, and orchestrated with Apache Airflow.

The pipeline follows a modern data engineering architecture with clear separation between ingestion, transformation, and orchestration layers.

---

## Data Source

API: OpenWeatherMap – Current Weather API  
URL: https://openweathermap.org/current

The API provides:

- Stable unique identifiers (`city_id`)
- Time-series data (`dt`)
- Multiple related entities suitable for relational modeling

---

## Data Model

### Entities

1. Cities

   - city_id (primary key)
   - name
   - country
   - latitude, longitude

2. Weather Observations
   - city_id (foreign key to cities)
   - timestamp
   - temperature
   - humidity
   - pressure
   - weather conditions

This structure enables referential integrity checks using dbt relationship tests.

---

## Database Schema Design

The PostgreSQL database is organized into three layers:

### raw schema

Stores data exactly as received from the API.

- raw.cities
- raw.weather

### staging schema (dbt-managed)

Cleans and standardizes raw data.

- staging.stg_cities
- staging.stg_weather

### mart schema (dbt-managed)

Final analytics-ready tables.

- mart.fct_daily_weather

---

## Pipeline Architecture

### Airflow DAGs (exactly two)

#### 1. openweather_ingestion_dag

- Scheduled daily
- Fetches data from the OpenWeather API
- Loads data into the raw schema
- Idempotent design:
  - Cities are upserted using city_id
  - Weather data is deleted and reloaded per ingestion date

#### 2. dbt_transformations_dag

- Scheduled daily
- Executes:
  - dbt run
  - dbt test
- Builds staging and mart schemas
- Runs all dbt data quality tests

---

## dbt Tests

The following dbt tests are implemented:

- not_null test on primary keys
- unique test on city_id
- relationships test between:
  - stg_weather.city_id → stg_cities.city_id

These tests ensure data quality and referential integrity.

---

## How to Run the Project

### Prerequisites

- Docker
- Docker Compose
- OpenWeather API key

---

### Environment Variables

Create a `.env` file in the project root:

OPENWEATHER_API_KEY=your_api_key_here

The `.env` file is not committed to the repository.

---

### Start Services

From the project root, run:

docker compose up -d

---

### Initialize Raw Tables (One-Time Setup)

docker exec -i openweather_postgres \
 psql -U airflow -d weather_db < sql/init_raw_tables.sql

---

### Access Airflow UI

Open the following URL in your browser:

http://localhost:8080

Login credentials:

- Username: admin
- Password: admin

---

### Run the Pipeline

1. Trigger the `openweather_ingestion_dag` and wait for it to complete successfully.
2. Trigger the `dbt_transformations_dag` to build staging and mart tables.

---

## Project Structure

.
├── docker-compose.yml
├── dags/
│ ├── openweather_ingestion_dag.py
│ └── dbt_transformations_dag.py
├── dbt/
│ ├── dbt_project.yml
│ ├── profiles.yml
│ └── models/
│ ├── sources.yml
│ ├── staging/
│ └── mart/
├── sql/
│ └── init_raw_tables.sql
├── .env
└── README.md

---

## Assignment Requirements Checklist

- External REST API used
- Two related entities
- Stable identifiers and timestamps
- Raw, staging, and mart schemas
- Idempotent ingestion
- dbt sources and transformations
- dbt tests (not null, unique, relationships)
- Exactly two Airflow DAGs
- Daily scheduling
- Fully reproducible with Docker

---

## Author

Akhjan  
Big Data Analytics – Final Project  
KBTU
