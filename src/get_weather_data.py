"""
Here we keep the function for retrieving
the data from the API, taking the date
as an input
"""

import requests

from constants import AMSTERDAM_GRID_CONFIG, API_USERNAME, API_PASSWORD, URL_GRID


class QueryTypeNotSupported(Exception):
    pass


class APIError(Exception):
    pass


def get_weather_grid_on_date(
    data_interval_start: str,
    data_interval_end: str,
    location_mode: str = "grid",
    location_config: str = AMSTERDAM_GRID_CONFIG,
    username: str = API_USERNAME,
    password: str = API_PASSWORD,
) -> dict:
    """
    Fetches hourly weather data for a grid over Amsterdam for a specific time interval.

    Parameters:
        data_interval_start  (str): Datetime in 'YYYY-MM-DDT00:00:00Z' format. Note: corresponds
            to the Airflow macro data_interval_start, which is the intended usage
        data_interval_end (str): Datetime in 'YYYY-MM-DDT00:00:00Z' format. Note: corresponds
            to the Airflow macro data_interval_end, which is the intended usage
        location_mode (str): indicates the location mode type we are querying here
        location_config (str): Coordinates configuration defining the location, as per API docs
        username (str): Meteomatics API username
        password (str): Meteomatics API password

    Returns:
        dict: Weather data or error message
    """

    if location_mode == "grid":
        url_to_query = (
            URL_GRID.replace("timestamp_interval_start", data_interval_start)
            .replace("timestamp_interval_end", data_interval_end)
            .replace("location_config", location_config)
        )

    else:
        raise QueryTypeNotSupported(
            "This type of location querying is not yet supported"
        )

    try:
        response = requests.get(url_to_query, auth=(username, password))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise APIError(f"The API query failed with the following issue: {str(e)}")
