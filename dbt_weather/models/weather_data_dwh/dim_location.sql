{{ config(
    materialized="table",
    unique_key='location_id'
) }}
-- note: we could use country as a partition or index key if we had a lot of data
-- note2: for the location id, we can hash the coords as a string

SELECT
    MD5(CAST(latitude AS VARCHAR) || ':' || CAST(longitude AS VARCHAR)) AS location_id,
    CAST(latitude AS FLOAT) AS location_latitude,
    CAST(longitude AS FLOAT) AS location_latitude
FROM {{ ref('weather_data') }}
GROUP BY 1,2,3
