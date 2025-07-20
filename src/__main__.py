"""
Here we keep the main() function that takes as an input
the timestamp interval start and end, and saves the data
as a csv in the configured location
"""

from src.get_weather_data import get_weather_grid_on_date


data_interval_start = '2025-07-15T00:00:00Z'
data_interval_end = '2025-07-17T00:00:00Z'

def main(data_interval_start : str, data_interval_end: str, data_storage_location: str) -> None:
    """Retrieve data from API, parse it into csv, save csv in location"""

    weather_data = get_weather_grid_on_date(
        data_interval_start ,
        data_interval_end
    )
