{{ config(
    materialized="table",
    unique_key='fact_id',
    partition_by='date',
    cluster_by='measurement_id'
) }}

-- note: we create the fact_id as a hash of
-- timestamp + location_id + measurement_id
-- at a later step, after we parse the data

WITH fact_base AS (
    SELECT
        timestamp AS fact_timestamp,
        CAST(DATE(timestamp) AS VARCHAR) AS date_string,
        MD5(CAST(latitude AS VARCHAR) || ':' || CAST(longitude AS VARCHAR)) AS location_id,
        CASE
            WHEN measurement = 't_2m:C' THEN 1
            WHEN measurement = 'relative_humidity_2m:p' THEN 2
            WHEN measurement = 'wind_speed_10m:ms' THEN 3
        ELSE NULL
        END AS measurement_id,
        value AS measurement_value
    FROM {{ ref('weather_data') }}
    GROUP BY 1,2,3,4,5
)

SELECT
    MD5(CAST(fact_timestamp AS VARCHAR) || ':' || location_id || ':' || CAST(measurement_id AS VARCHAR)) AS fact_id,
    fact_timestamp,
    date_string,
    location_id,
    measurement_id,
    measurement_value
FROM fact_base
