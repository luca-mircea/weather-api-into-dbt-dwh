import pytest
import pandas as pd
from transform_weather_data import process_weather_data


# viva la ChatGPT


@pytest.fixture
def sample_weather_data():
    return {
        "version": "3.0",
        "user": "companynameltd",
        "dateGenerated": "2025-07-21T19:02:30Z",
        "status": "OK",
        "data": [
            {
                "parameter": "t_2m:C",
                "coordinates": [
                    {
                        "lat": 51.5,
                        "lon": 4.5,
                        "dates": [
                            {"date": "2025-07-20T00:00:00Z", "value": 18.7},
                            {"date": "2025-07-20T01:00:00Z", "value": 18.6},
                            {"date": "2025-07-20T02:00:00Z", "value": 18.1},
                        ],
                    }
                ],
            }
        ],
    }


def test_process_weather_data_output(sample_weather_data):
    df = process_weather_data(sample_weather_data)

    # Check structure
    expected_columns = {
        "latitude",
        "longitude",
        "timestamp",
        "value",
        "measurement",
        "retrieved_at",
    }
    assert set(df.columns) == expected_columns

    # Check number of rows = number of timestamps
    assert len(df) == 3

    # Check values in one row
    row = df.iloc[0]
    assert row["latitude"] == 51.5
    assert row["longitude"] == 4.5
    assert row["timestamp"] == "2025-07-20T00:00:00Z"
    assert row["value"] == 18.7
    assert row["measurement"] == "t_2m:C"
    assert row["retrieved_at"] == "2025-07-21T19:02:30Z"
