from airflow.sdk.definitions.asset import Dataset

PROCESSED_PATH = "/opt/airflow/data/processed"
RAW_PATH = "/opt/airflow/data/raw"
PROCESSED_DATASET = Dataset(PROCESSED_PATH)