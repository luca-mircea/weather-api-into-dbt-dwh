# weather-api-into-dbt-dwh
Solution for technical challenge showcasing a Python API ingestion + dbt transformation into a Kimball DWH

## Running instructions

Clone the repo:
```
git clone https://github.com/luca-mircea/weather-api-into-dbt-dwh.git
```

Create a `.env` file using the `example_env` template in `src/example_env`, place it within the `src` folder like so:
<img width="408" height="462" alt="image" src="https://github.com/user-attachments/assets/fb116f96-f7e0-4f60-9125-858087967e11" />

Build the container:

```
docker build . -t weather_dbt
```

Then you can run it with the following commands:
```
# simple run for ingesting the data from the API, saving it locally; the function uses default parameters:
docker run weather_dbt python src

# you can also pass the data interval start and end, suitable for scheduling with Airflow:
docker run weather_dbt python src --data_interval_start "2025-07-20T00:00:00" --data_interval_end "2025-07-21T00:00:00"

# finally, to run the entire dbt part:
docker run weather_dbt bash -c "dbt seed --profiles-dir /app/dbt_weather/profiles && dbt run --profiles-dir /app/dbt_weather/profiles && dbt test --profiles-dir /app/dbt_weather/profiles"
```

**Note:** if I had more time, I'd build a mock database with an interface, like shown in [this repo](https://github.com/luca-mircea/holidays-api), which would enable the user to query the DWH and see the results of different queries

## Project structure + contents
There are two main parts to this assignment + supporting documents. The important bits are the `src` and `dbt_weather` folders and they are supported by:
- the folder `dag` which contains the mock `dag.py` that illustrates Airflow orchestration for the app developed in this project, assuming that it is to be placed in an Airflow repo that has access to the docker with the application.
- the folder `data_model` which contains an image of the data model, which can also be seen below
- the `tests` folder is required for the unit tests (currently there is only 1, written with help from ChatGPT)
- the `Dockerfile` which builds the container that runs the app
- various configs: `.dockerignore`, `.gitignore`, `pytest.ini`, `dbt_project.yml`, `requirements.txt`
- the `.github` folder, with a GitHub Action that checks whether the code is linted and passes the tests

![weather_dwh](https://github.com/user-attachments/assets/6d13236e-1f36-4fe3-9696-93b5c09f6049)

The `src` folder:
This is the Python application code, which pulls data from the API, reshapes it by flattening the ultra-nested response, and saves it as a `.csv` file in the seeds folder of dbt. 
Under regular circumstances, this data would be saved in the raw format in some storage location, like an AWS S3 bucket (task 1), and from there a different function would read it and transform it into something tabular that can be saved as a `.csv` (task 2). However, given the scope of the assignment and the context, I opted to do everything in one go (task 1 + task 2 in one).
More or less the entire config is set up in `constants.py`, and `get_weather_data.py` + `transform_weather_data.py` contain supporting functions.
`__main__.py` puts everything together, making use of default Python naming conventions to run the code with minimal typing. The app supports default dates, but it can also accept parameters for the `data_interval_start` and `data_interval_end`, which correspond to Airflow macros that can be used to make it idempotent, run back-fills, etc. with no additional modifications to the existing code.

**Please note:** to run the code you need to provide API credentials in the `.env` file that can be obtained by filling in the `example_env` present in the `src` folder.

The `dbt_weather` folder:
This is where all the dbt code is kept, except for the `dbt_project.yml` that needs to be outside of the folder. It contains:
- 2 macros used for hashing data to create unique IDs
- 4 `.sql` models that produce the tables required by the assignment
- 4 `.yml` configurations for the models, containing column descriptions and test configurations
- 1 seed with the weather data.

If I had more time I would:
- add 1 additional seed with location data that can be used to add city + country
- create custom tests

Under normal circumstances, there would be a proper connection to a data warehouse which would run the actual processing of the data so it can take advantage of the scalable compute.

## Assumptions + design choices

My biggest assumptions are about the Airflow config, since it's different in every company, and deploying it locally felt somewhat overkill for the current assignment. Therefore, I assumed a setup that uses a service like AWS ECR to store containers that can be run from within the `dag.py`, based on how this was set up at a previous workplace. Either way, I figured the important part is to create and then orchestrate the multiple tasks (the assignment description suggested 4, but I combined them into 2, separated by what's needed to run them, either python or dbt) more than the exact configuration.

I used `__main__.py` to make the `python src` command as neat as possible, but I could also have opted for a design where I create two different functions here, one which retrieves the data from the API and one which processes it, which could have made more sense in a production context where we e.g. want to minimize API calls and follow engineering best practices, where every function does exactly one thing. Nonetheless, in this particular context this separation would not have done much in practical terms (beside showing that I know why to make it), which is why I opted to have a nice run-time command instead.

The wording of the assignment also gave me the impression that there was an intention for the dbt script to be run from within Python - this could also have been done and this function added to the entrypoints, creating another neat Python function to be run from outside the container. However, I opted to run dbt as a standalone program, independent of Python, because it is often run from a separate repo and connected to the DWH, such that it can take maximum advantage of DWH functionality to distribute workloads, scale compute, etc..
