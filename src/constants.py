# Here we keep various constants, like
# API parameters, naming configs, as well
# as data from the .env, such as the password
# of the API account

from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path('src/.env')
load_dotenv(dotenv_path=env_path)

load_dotenv()

# API parameters
# Amsterdam center coordinates
lat_center = 52.3676
lon_center = 4.9041

lat_min = lat_center - 0.02
lat_max = lat_center + 0.02
lon_min = lon_center - 0.02
lon_max = lon_center + 0.02
lat_n = lon_n = 5  # 5 points in each direction

AMSTERDAM_GRID_CONFIG = f"{lat_min}-{lat_max}:{lat_n}x{lon_min}-{lon_max}:{lon_n}"

# Weather parameters

list_of_weather_params = [
    "t_2m:C",
    "relative_humidity_2m:p",
    "wind_speed_10m:ms",
    "moon_phase:idx",
]

parameters = ",".join(list_of_weather_params)

# URL
# for a grid
URL_GRID = (
    f"https://api.meteomatics.com/timestamp_interval_start--timestamp_interval_end:PT1H"
    f"/{parameters}/location_config/grid/json"
)

# note: PT1H means hourly data

# note: later on we could extend this to retrieving the data
# simply for a pair of coords, in which case we'd use
# a different URL

# API creds

API_USERNAME = os.getenv("API_USERNAME")
API_PASSWORD = os.getenv("API_PASSWORD")
