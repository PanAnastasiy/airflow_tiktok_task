from airflow.sdk.definitions.asset import Dataset


PROCESSED_PATH = "/opt/airflow/data/processed"
PROCESSED_DATASET = Dataset(PROCESSED_PATH)
MONGO_CONN_URI = "mongodb://localhost:27017"
MONGO_DB = "tiktok_db"
MONGO_COLLECTION = "tiktok_processed"
RAW_PATH = "/opt/airflow/data/raw"
MONGO_URI = "mongodb://mongo:27017"