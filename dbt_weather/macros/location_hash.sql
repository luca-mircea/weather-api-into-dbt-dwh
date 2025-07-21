{% macro location_hash(latitude, longitude) %}

MD5(CAST(latitude AS VARCHAR) || ':' || CAST(longitude AS VARCHAR))

{% endmacro %}