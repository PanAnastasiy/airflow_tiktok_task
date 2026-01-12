import os
from datetime import datetime

from airflow.sdk import dag
from dotenv import load_dotenv

from core.airflow.dags.include.consts import PROCESSED_DATASET, PROCESSED_PATH
from core.airflow.dags.include.tasks.load_to_mongo_tasks import load

load_dotenv()


@dag(
    dag_id="load_tiktok_to_mongo",
    start_date=datetime(2025, 1, 1),
    schedule=[PROCESSED_DATASET],
    catchup=False,
    tags=["tiktok", "mongo"],
)
def load_to_mongo():
    """
    DAG: Load TikTok Processed CSV Files into MongoDB.

    Workflow:
    1. List all processed CSV files from the configured PROCESSED_PATH.
    2. For each file ending with "_processed.csv":
       - Call the 'load' task to upload the CSV content to MongoDB.

    Requirements:
    - Environment variables loaded from `.env`.
    - PROCESSED_DATASET and PROCESSED_PATH defined in `include.consts`.
    - `load` task implemented in `include.tasks.load_to_mongo_tasks`.
    """

    processed_files = [
        os.path.join(PROCESSED_PATH, f)
        for f in os.listdir(PROCESSED_PATH)
        if f.endswith("_processed.csv")
    ]

    for file_path in processed_files:
        load(file_path)


load_to_mongo()
