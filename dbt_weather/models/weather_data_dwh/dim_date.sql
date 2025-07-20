{{ config(
    materialized="table",
    unique_key='date'
) }}

WITH base_dates AS (
    SELECT
        DATE(timestamp) AS date_string
    FROM {{ ref('weather_data') }}
    GROUP BY 1
)

SELECT
    date_string,
    EXTRACT(DOW FROM date_string) AS day_of_week,  -- Sunday = 0, Saturday = 6
    EXTRACT(DAY FROM date_string) AS day_int,
    EXTRACT(MONTH FROM date_string) AS month_int,
    EXTRACT(YEAR FROM date_string) AS year_int,
FROM base_dates
