select
    city_id,
    weather_ts,
    temperature,
    humidity,
    pressure,
    weather_main
from {{ source('openweather_raw', 'weather') }}
