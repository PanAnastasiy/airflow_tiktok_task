import os
from datetime import datetime
from airflow.providers.standard.sensors.filesystem import FileSensor
from airflow.sdk import task, dag

from include.consts import PROCESSED_PATH, RAW_PATH


@dag(dag_id="process_tiktok_data_dag", start_date=datetime(2025,1,1), schedule=None, catchup=False)
def process_tiktok_data():

    @task
    def check_file(file_path: str):

        from include.file_handler import FileHandler
        if FileHandler.is_empty(file_path):
            return "empty_file"
        return "process_file"

    @task
    def process_file(file_path: str):
        from include.csv_handler import CSVHandler
        base_name = os.path.basename(file_path).replace(".csv", "")
        output_path = os.path.join(PROCESSED_PATH, f"{base_name}_processed.csv")
        CSVHandler(file_path).replace_nulls().sort_by_date().clean_content().save(output_path)
        return output_path

    @task
    def log_empty(file_path: str):
        print(f"File {file_path} is empty")

    files = [os.path.join(RAW_PATH, f) for f in os.listdir(RAW_PATH) if f.endswith(".csv")]

    for f in files:
        sensor = FileSensor(task_id=f"wait_{os.path.basename(f)}", filepath=f, poke_interval=10, timeout=300)
        branch = check_file(f)
        empty = log_empty(f)
        processed = process_file(f)
        sensor >> branch
        branch >> empty
        branch >> processed

process_tiktok_data_dag = process_tiktok_data()
