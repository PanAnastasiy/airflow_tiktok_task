from typing import Any, Dict, List, Optional

import pandas as pd
from pymongo import MongoClient, errors


class MongoHandler:
    """
    MongoHandler provides methods to connect to MongoDB, insert documents,
    load data from CSV files, and close the connection.
    """

    def __init__(
        self,
        uri: str = "mongodb://localhost:27017/",
        db_name: str = "test_db",
    ):
        """
        Initialize MongoHandler with URI and database name.

        Args:
            uri (str): MongoDB connection URI.
            db_name (str): Target database name.
        """
        self.uri = uri
        self.db_name = db_name
        self.client: Optional[MongoClient] = None
        self.db: Optional[Any] = None

    def connect(self) -> None:
        """
        Connect to MongoDB and initialize the database object.
        """
        self.client = MongoClient(self.uri)
        self.db = self.client[self.db_name]
        print(f"[INFO] Connected to MongoDB at {self.uri}, DB: {self.db_name}")

    def insert_many(self, collection: str, data: List[Dict[str, Any]]) -> Optional[List[Any]]:
        """
        Insert multiple documents into a MongoDB collection.

        Args:
            collection (str): Name of the MongoDB collection.
            data (List[Dict[str, Any]]): List of documents to insert.

        Returns:
            Optional[List[Any]]: List of inserted document IDs or None on failure.
        """
        if self.db is None:
            print("[ERROR] No DB connection. Call connect() first")
            return None
        if not data:
            print("[WARNING] No data provided to insert")
            return None

        try:
            result = self.db[collection].insert_many(data)
            print(f"[INFO] Inserted {len(result.inserted_ids)} documents.")
            return result.inserted_ids
        except errors.PyMongoError as e:
            print(f"[ERROR] Insert many error: {e}")
            return None

    def load_csv(self, collection: str, file_path: str) -> Optional[List[Any]]:
        """
        Load data from a CSV file and insert it into a MongoDB collection.

        Args:
            collection (str): Name of the MongoDB collection.
            file_path (str): Path to the CSV file.

        Returns:
            Optional[List[Any]]: List of inserted document IDs or None if CSV is empty.
        """
        if self.db is None:
            print("[ERROR] No DB connection. Call connect() first")
            return None

        df = pd.read_csv(file_path)
        if df.empty:
            print(f"[WARNING] No data in CSV file: {file_path}")
            return None

        return self.insert_many(collection, df.to_dict(orient="records"))

    def close(self) -> None:
        """
        Close the MongoDB client connection.
        """
        if self.client is not None:
            self.client.close()
            print("[INFO] MongoDB connection closed")
