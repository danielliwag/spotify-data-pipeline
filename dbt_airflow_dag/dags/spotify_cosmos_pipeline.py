import sys
from datetime import datetime
from pathlib import Path
from airflow.decorators import dag
from airflow.operators.python import PythonOperator
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig, RenderConfig
from cosmos.constants import LoadMode
from cosmos.profiles import PostgresUserPasswordProfileMapping

# Resolve paths relative to this DAG file's location inside Astro
DAG_FOLDER = Path(__file__).parent
sys.path.append(str(DAG_FOLDER / "src"))

from spotify_pipeline import run_pipeline

# Point Cosmos to dags/spotify_dbt
DBT_PROJECT_PATH = DAG_FOLDER / "spotify_dbt"

@dag(
    start_date=datetime(2026, 5, 17),
    schedule="@daily",
    catchup=False,
    tags=["spotify", "dbt"],
)
def spotify_cosmos_pipeline():

    # Task 1: Runs your custom script to grab Spotify data and dump it into Postgres
    extract_and_load_raw = PythonOperator(
        task_id="extract_and_load_raw",
        python_callable=run_pipeline
    )

    # Task 2: Cosmos dynamically turns your dbt models into visual check-steps
    transform_dbt = DbtTaskGroup(
        group_id="dbt_transforms",
        project_config=ProjectConfig(DBT_PROJECT_PATH.as_posix()),
        profile_config=ProfileConfig(
            profile_name="spotify_profile", 
            target_name="dev",
            profile_mapping=PostgresUserPasswordProfileMapping(
                conn_id="my_postgres_connection", 
                profile_args={"schema": "daniel"},
            ),
        ),
        execution_config=ExecutionConfig(
            dbt_executable_path="/usr/local/airflow/dbt_venv/bin/dbt"
        )
    )

    extract_and_load_raw >> transform_dbt


spotify_cosmos_pipeline()