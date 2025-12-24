
  create view "weather_db"."public_staging"."stg_cities__dbt_tmp"
    
    
  as (
    select
    city_id,
    name,
    country,
    lat,
    lon
from "weather_db"."raw"."cities"
  );