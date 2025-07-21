"""
Note: normally this goes in another repo where keep
all of Airflow. Therefore, the code in here is more
illustrative of what that would look like.

I am assuming that we could run the container
of this project directly on Airflow, since this
is how it was done at a previous job (the docker
would live on the AWS ECR and be collected from
there when the DAG was deployed).
"""

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime
from airflow.utils.task_group import TaskGroup

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

with DAG(
    dag_id='weather_dbt_k8s_pipeline',
    default_args=default_args,
    schedule_interval="0 7 * * *",  # 7 am every day
    catchup=True,  # we want all weather for all time
    description='Run weather pipeline using KubernetesPodOperator',
) as dag:

    # Task 1: Retrieve weather data
    retrieve_weather_data = KubernetesPodOperator(
        task_id='retrieve_weather_data',
        name='retrieve-weather-data',
        namespace='default',
        image='123456789012.dkr.ecr.us-east-1.amazonaws.com/weather_dbt:latest',
        cmds=[
            'python', 'src',
            '--data_interval_start', '{{ data_interval_start }}',
            '--data_interval_end', '{{ data_interval_end }}'],
        get_logs=True,
        is_delete_operator_pod=True,
        image_pull_policy='Always'
    )

    # Task 2: Run dbt transformations to update the weather DWH
    run_weather_dwh = KubernetesPodOperator(
        task_id='run_weather_dwh',
        name='run-weather-dwh',
        namespace='default',
        image='123456789012.dkr.ecr.us-east-1.amazonaws.com/weather_dbt:latest',
        cmds=[
            'dbt', 'seed', '--profiles-dir', '/app/dbt_weather/profiles',
            ' && ', 'dbt', 'run', '--profiles-dir', '/app/dbt_weather/profiles'
            ],
        get_logs=True,
        is_delete_operator_pod=True,
        image_pull_policy='Always',
    )

    retrieve_weather_data >> run_weather_dwh
