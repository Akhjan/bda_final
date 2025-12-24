select
    city_id,
    name,
    country,
    lat,
    lon
from {{ source('openweather_raw', 'cities') }}
