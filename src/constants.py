# Here we keep various constants, like
# API parameters, naming configs, as well
# as data from the .env, such as the password
# of the API account

from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path("src/.env")
load_dotenv(dotenv_path=env_path)

load_dotenv()

# API parameters

TIMESTAMP_FORMAT = "insert_timestamp_here.000+00:00"
# note: insert_timestamp_here must be a string
# with the format YYYY-MM-DDTHH:SS:MM

lat_1 = 52.5
lon_1 = 4.5

lat_2 = 51.5
lon_2 = 5.5
spacing_config = "0.2,0.2"
AMSTERDAM_GRID_CONFIG = f"{lat_1},{lon_1}_{lat_2},{lon_2}:{spacing_config}"

# Weather parameters

list_of_weather_params = ["t_2m:C", "relative_humidity_2m:p", "wind_speed_10m:ms"]

parameters = ",".join(list_of_weather_params)

# URL
# for a grid
URL_GRID = (
    f"https://api.meteomatics.com/timestamp_interval_start--timestamp_interval_end:PT1H/"
    f"{parameters}/location_config/json?model=mix"
)

# note: PT1H means hourly data

# note: later on we could extend this to retrieving the data
# simply for a pair of coords, in which case we'd use
# a different URL

# API creds

API_USERNAME = os.getenv("API_USERNAME")
API_PASSWORD = os.getenv("API_PASSWORD")

# Path for saving the raw weather data as a csv
PATH_TO_DATA = "dbt_weather/seeds"
