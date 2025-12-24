select
    city_id,
    date(weather_ts) as weather_date,
    avg(temperature) as avg_temperature,
    avg(humidity) as avg_humidity,
    avg(pressure) as avg_pressure
from "weather_db"."public_staging"."stg_weather"
group by 1, 2