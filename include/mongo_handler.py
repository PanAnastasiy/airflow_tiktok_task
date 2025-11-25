from typing import Any, Dict, List, Optional
from pymongo import MongoClient
import pandas as pd
from utils.design import Message, Color

class MongoHandler:
    def __init__(self, uri: str = "mongodb://localhost:27017/", db_name: str = "test_db"):
        self.uri = uri
        self.db_name = db_name
        self.client: Optional[MongoClient] = None
        self.db = None

    def connect(self):
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            Message.print_message(
                f"Connected to MongoDB at {self.uri}, DB: {self.db_name}",
                Color.GREEN,
                Color.LIGHT_WHITE,
            )
        except Exception as e:
            Message.print_message(f"MongoDB connection error: {e}", Color.RED, Color.LIGHT_WHITE)
            self.client = None

    def insert_one(self, collection: str, data: Dict[str, Any]):
        if not self.db:
            Message.print_message("No DB connection. Call connect() first", Color.RED, Color.LIGHT_WHITE)
            return None
        try:
            result = self.db[collection].insert_one(data)
            Message.print_message(f"✅ Inserted document ID: {result.inserted_id}", Color.BLUE, Color.LIGHT_WHITE)
            return result.inserted_id
        except Exception as e:
            Message.print_message(f"❌ Insert error: {e}", Color.RED, Color.LIGHT_WHITE)
            return None

    def insert_many(self, collection: str, data: List[Dict[str, Any]]):
        if not self.db:
            Message.print_message("No DB connection. Call connect() first", Color.RED, Color.LIGHT_WHITE)
            return None
        try:
            result = self.db[collection].insert_many(data)
            Message.print_message(f"✅ Inserted {len(result.inserted_ids)} documents.", Color.BLUE, Color.LIGHT_WHITE)
            return result.inserted_ids
        except Exception as e:
            Message.print_message(f"❌ Insert many error: {e}", Color.RED, Color.LIGHT_WHITE)
            return None

    def find_one(self, collection: str, query: Dict[str, Any]):
        if not self.db:
            Message.print_message("No DB connection. Call connect() first", Color.RED, Color.LIGHT_WHITE)
            return None
        try:
            result = self.db[collection].find_one(query)
            Message.print_message(f"🔎 Found document: {result}", Color.BLUE, Color.LIGHT_WHITE)
            return result
        except Exception as e:
            Message.print_message(f"❌ Find error: {e}", Color.RED, Color.LIGHT_WHITE)
            return None

    def load_csv(self, collection: str, file_path: str):
        """Вставка данных из CSV файла в коллекцию"""
        df = pd.read_csv(file_path)
        return self.insert_many(collection, df.to_dict(orient="records"))

    def close(self):
        if self.client:
            self.client.close()
            Message.print_message("MongoDB connection closed", Color.GREEN, Color.LIGHT_WHITE)
