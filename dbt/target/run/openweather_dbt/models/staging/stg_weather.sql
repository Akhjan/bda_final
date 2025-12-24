
  create view "weather_db"."public_staging"."stg_weather__dbt_tmp"
    
    
  as (
    select
    city_id,
    weather_ts,
    temperature,
    humidity,
    pressure,
    weather_main
from "weather_db"."raw"."weather"
  );