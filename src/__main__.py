"""
Here we keep the main() function that takes as an input
the timestamp interval start and end, and saves the data
as a csv in the configured location
"""
import argparse
from datetime import datetime, timedelta

from get_weather_data import get_weather_grid_on_date
from constants import PATH_TO_DATA, TIMESTAMP_FORMAT
from transform_weather_data import process_weather_data, load_weather_data

# note: setting up default values for ease of running
yesterday = datetime.date(datetime.today() - timedelta(days=1))
today = datetime.date(datetime.today())
data_interval_start_default = f"{yesterday}T00:00:00"
data_interval_end_default = f"{today}T00:00:00"


def main(
    data_interval_start: str = data_interval_start_default,
    data_interval_end: str = data_interval_end_default,
    data_storage_location: str = PATH_TO_DATA,
) -> None:
    """Retrieve data from API, parse it into csv, save csv in location"""

    weather_data = get_weather_grid_on_date(
        TIMESTAMP_FORMAT.replace("insert_timestamp_here", data_interval_start),
        TIMESTAMP_FORMAT.replace("insert_timestamp_here", data_interval_end),
    )

    flat_weather_data = process_weather_data(weather_data)

    load_weather_data(flat_weather_data, data_storage_location)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # note: we might even format them before feeding into the main
    # if we don't like the way Airflow injects it
    parser.add_argument("--data_interval_start", required=False)
    parser.add_argument("--data_interval_end", required=False)
    args = parser.parse_args()

    main(args.data_interval_start, args.data_interval_end)
