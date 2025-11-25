import os

from airflow.sdk import task

from include.handlers.mongo_handler import MongoHandler


@task
def load(file_path: str) -> str:
    """
    Load a CSV file into MongoDB using MongoHandler.

    Args:
        file_path (str): Path to the CSV file to load.

    Returns:
        str: Message indicating success or failure of the load operation.
    """
    mongo = MongoHandler(
        uri=os.getenv("MONGO_CONN_URI"), db_name=os.getenv("MONGO_DB")
    )
    mongo.connect()
    result = mongo.load_csv(os.getenv("MONGO_COLLECTION"), file_path)
    mongo.close()

    if result:
        return f"{len(result)} records loaded from {file_path}"
    return f"Failed to load {file_path}"
