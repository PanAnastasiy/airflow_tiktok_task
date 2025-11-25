import os
from datetime import datetime
from airflow.sdk import dag, task
from include.consts import PROCESSED_DATASET, MONGO_CONN_URI, MONGO_DB, MONGO_COLLECTION, PROCESSED_PATH
from include.mongo_handler import MongoHandler

@dag(
    dag_id="load_tiktok_to_mongo",
    start_date=datetime(2025, 1, 1),
    schedule=[PROCESSED_DATASET],
    catchup=False,
    tags=["tiktok", "mongo"],
)
def load_to_mongo():

    @task
    def load(file_path: str):
        mongo = MongoHandler(uri=MONGO_CONN_URI, db_name=MONGO_DB)
        mongo.connect()
        result = mongo.load_csv(MONGO_COLLECTION, file_path)
        mongo.close()
        return f"{len(result)} records loaded from {file_path}" if result else f"Failed to load {file_path}"

    # Берем все обработанные CSV
    processed_files = [
        os.path.join(PROCESSED_PATH, f)
        for f in os.listdir(PROCESSED_PATH)
        if f.endswith("_processed.csv")
    ]

    for f in processed_files:
        load(f)


load_to_mongo_dag = load_to_mongo()
