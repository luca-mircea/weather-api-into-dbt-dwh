{% macro weather_fact_id_hash(fact_timestamp, location_id, measurement_id) %}

MD5(CAST(fact_timestamp AS VARCHAR) || ':' || location_id || ':' || CAST(measurement_id AS VARCHAR))

{% endmacro %}