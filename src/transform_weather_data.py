"""
Here we keep the function for transforming
the raw data, that comes as a dict, into
a csv file that we load as a seed in
the dbt folder
"""

import pandas as pd

from constants import PATH_TO_DATA


def process_weather_data(weather_data: dict) -> pd.DataFrame:
    """We crunch the dict into a csv to be saved in the dbt folder"""

    # create df to hold values
    raw_weather_data = pd.DataFrame()

    # 1st layer of unpacking: data + metadata
    date_retrieved = weather_data["dateGenerated"]
    raw_weather_location_data = weather_data["data"]

    # 2nd layer of unpacking: location * date values into dataframes, automatically scaling
    # for additional measurements added in the future
    measurements = [
        measurement["parameter"] for measurement in raw_weather_location_data
    ]
    location_date_values = [
        coordinates["coordinates"] for coordinates in raw_weather_location_data
    ]

    for parameter_number in range(len(measurements)):
        measure_name = measurements[parameter_number]
        location_date_data = location_date_values[parameter_number]

        for location_index in range(len(location_date_data)):
            current_location = location_date_data[location_index]

            current_lat = current_location["lat"]
            current_lon = current_location["lon"]
            current_date_values = current_location["dates"]

            for date_index in range(len(current_date_values)):
                current_date_value = current_date_values[date_index]

                current_datetime = current_date_value["date"]
                current_value = current_date_value["value"]

                current_row_df = pd.DataFrame(
                    {
                        "latitude": current_lat,
                        "longitude": current_lon,
                        "timestamp": current_datetime,
                        "value": current_value,
                        "measurement": measure_name,
                    },
                    index=[0],
                )

                raw_weather_data = pd.concat(
                    [raw_weather_data, current_row_df], ignore_index=True, axis=0
                )

    raw_weather_data["retrieved_at"] = date_retrieved

    return raw_weather_data


def load_weather_data(
    raw_weather_data: pd.DataFrame, path_to_upload: str = PATH_TO_DATA
) -> None:
    """Load the dataframe as a csv file into the dbt/seeds path"""
    # note: under normal circumstances we would save the file
    # with the date in the name, e.g. "weather_data_2025-07-20.csv".
    # however, given how seeds work in dbt, this is a bit too
    # complicated, so I won't implement it for now
    raw_weather_data.to_csv(f"{path_to_upload}/weather_data.csv", index=False)

    print("The data has been successfully loaded into dbt/seeds")
