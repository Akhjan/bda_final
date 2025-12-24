from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
import requests
import os

CITIES = ["London", "Almaty", "New York", "Tokyo"]

def fetch_and_load_weather(**context):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    pg = PostgresHook(postgres_conn_id="postgres_default")
    conn = pg.get_conn()
    cur = conn.cursor()

    today = datetime.utcnow().date()

    # idempotency: delete today's weather
    cur.execute(
        "DELETE FROM raw.weather WHERE ingestion_date = %s",
        (today,)
    )

    for city in CITIES:
        resp = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": city,
                "appid": api_key
            },
            timeout=30
        )
        data = resp.json()

        city_id = data["id"]

        # UPSERT city
        cur.execute("""
            INSERT INTO raw.cities (city_id, name, country, lat, lon, ingestion_date)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (city_id)
            DO UPDATE SET
              name = EXCLUDED.name,
              country = EXCLUDED.country,
              lat = EXCLUDED.lat,
              lon = EXCLUDED.lon,
              ingestion_date = EXCLUDED.ingestion_date
        """, (
            city_id,
            data["name"],
            data["sys"]["country"],
            data["coord"]["lat"],
            data["coord"]["lon"],
            today
        ))

        # INSERT weather
        cur.execute("""
            INSERT INTO raw.weather
            (city_id, weather_ts, temperature, humidity, pressure,
             weather_main, weather_desc, ingestion_date)
            VALUES (%s, to_timestamp(%s), %s, %s, %s, %s, %s, %s)
        """, (
            city_id,
            data["dt"],
            data["main"]["temp"],
            data["main"]["humidity"],
            data["main"]["pressure"],
            data["weather"][0]["main"],
            data["weather"][0]["description"],
            today
        ))

    conn.commit()
    cur.close()
    conn.close()

with DAG(
    dag_id="openweather_ingestion_dag",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["openweather", "ingestion"],
) as dag:

    ingest = PythonOperator(
        task_id="fetch_and_load_weather",
        python_callable=fetch_and_load_weather
    )

    ingest
