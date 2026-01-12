import os
from datetime import datetime

from airflow.providers.standard.sensors.filesystem import FileSensor
from airflow.sdk import dag

from core.airflow.dags.include.consts import RAW_PATH
from core.airflow.dags.include.tasks.process_tiktok_data_tasks import (
    check_file_empty,
    extract_data,
    file_is_empty,
    load_data,
    transform_group,
)


@dag(
    dag_id="process_tiktok_data_dag",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["etl", "tiktok"],
)
def process_tiktok_data_dag():
    """
    DAG: Process TikTok CSV Data.

    Workflow:
    1. Wait for the TikTok CSV file to appear using FileSensor.
    2. Check if the file is empty using a branching task.
       - If empty, execute `file_is_empty`.
       - Otherwise, continue processing.
    3. Extract data from the CSV into a DataFrame.
    4. Transform/clean the DataFrame using `transform_group`.
    5. Load the cleaned data using `load_data`.

    Notes:
    - RAW_PATH defines the folder where the raw CSV is stored.
    - All task functions are implemented in `process_tiktok_data_tasks`.
    """

    wait_file = FileSensor(
        task_id="wait_for_file",
        filepath=os.path.join(RAW_PATH, "tiktok_data.csv"),
        poke_interval=10,
        timeout=3600,
        mode="poke",
        fs_conn_id="fs_default",
    )

    file_path = os.path.join(RAW_PATH, "tiktok_data.csv")

    # Branching task to check if the file is empty
    branch = check_file_empty(file_path)

    # Task executed if file is empty
    empty_task = file_is_empty()

    # Extract CSV data into a DataFrame
    data_df = extract_data(file_path)

    # Transform and clean the DataFrame
    cleaned_df = transform_group(data_df)

    # Load the cleaned data to the target destination
    output_file = load_data(cleaned_df, file_path)

    wait_file >> branch
    branch >> [empty_task, data_df]
    data_df >> cleaned_df >> output_file


process_tiktok_data_dag()
