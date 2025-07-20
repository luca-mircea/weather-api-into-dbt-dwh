{{ config(
    materialized="table",
    unique_key='measurement_id'
) }}

-- note: we build this one by hand since there are so few of them
-- and we need to parse the units and retrieve the descriptions manually

SELECT
    1 AS measurement_id,
    't_2m' AS measure_string,
    'C' AS unit_of_measurement,
    'Gives the instantaneous temperature at the indicated level above ground or pressure level in the corresponding unit. Standard height for surface air temperature is 2m.' AS measurement_description
UNION ALL
SELECT
    2 AS measurement_id,
    'relative_humidity_2m' AS measure_string,
    'percent' AS unit_of_measurement,
    'Gives the instantaneous value of the relative humidity in percent at the indicated level above ground or pressure level. Standard height for surface relative humidity is 2m.' AS measurement_description
UNION ALL
SELECT
    3 AS measurement_id,
    'wind_speed_10m' AS measure_string,
    'meters_per_second' AS unit_of_measurement,
    'Gives the instantaneous wind speed at the indicated level above ground or pressure level. Standard height for surface wind speed is 10m.' AS measurement_description

