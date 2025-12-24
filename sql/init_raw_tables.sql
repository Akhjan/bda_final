-- Create raw schema
CREATE SCHEMA IF NOT EXISTS raw;

-- Cities dimension
CREATE TABLE IF NOT EXISTS raw.cities (
    city_id INTEGER PRIMARY KEY,
    name TEXT,
    country TEXT,
    lat FLOAT,
    lon FLOAT,
    ingestion_date DATE
);

-- Weather facts
CREATE TABLE IF NOT EXISTS raw.weather (
    city_id INTEGER,
    weather_ts TIMESTAMP,
    temperature FLOAT,
    humidity INTEGER,
    pressure INTEGER,
    weather_main TEXT,
    weather_desc TEXT,
    ingestion_date DATE
);
