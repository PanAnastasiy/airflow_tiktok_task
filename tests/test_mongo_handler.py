import mongomock
import pandas as pd
import pytest

from core.airflow.dags.utils.handlers.mongo_handler import MongoHandler


@pytest.fixture
def mongo_mock(monkeypatch):
    """
    Replace MongoClient with mongomock for testing.
    """
    mock_client = mongomock.MongoClient()
    monkeypatch.setattr("utils.handlers.mongo_handler.MongoClient", lambda uri: mock_client)
    return mock_client


def test_connect_sets_db(mongo_mock):
    handler = MongoHandler(uri="mongodb://test:27017", db_name="test_db")
    handler.connect()
    assert handler.db is not None
    assert handler.client is not None
    assert handler.db.name == "test_db"


def test_insert_many_inserts_documents(mongo_mock):
    handler = MongoHandler(db_name="test_db")
    handler.connect()

    data = [{"name": "Alice"}, {"name": "Bob"}]
    inserted_ids = handler.insert_many("users", data)

    assert inserted_ids is not None
    assert len(inserted_ids) == 2
    # Verify documents in collection
    docs = list(handler.db["users"].find({}))
    assert len(docs) == 2
    assert docs[0]["name"] in ["Alice", "Bob"]


def test_insert_many_no_db(monkeypatch):
    handler = MongoHandler()
    # Do not call connect()
    result = handler.insert_many("users", [{"name": "Alice"}])
    assert result is None


def test_insert_many_empty_data(mongo_mock):
    handler = MongoHandler()
    handler.connect()
    result = handler.insert_many("users", [])
    assert result is None


def test_load_csv_creates_documents(tmp_path, mongo_mock):
    handler = MongoHandler()
    handler.connect()

    # Create temporary CSV file
    csv_file = tmp_path / "test.csv"
    df = pd.DataFrame({"name": ["Alice", "Bob"]})
    df.to_csv(csv_file, index=False)

    inserted_ids = handler.load_csv("users", str(csv_file))
    assert inserted_ids is not None
    assert len(inserted_ids) == 2
    docs = list(handler.db["users"].find({}))
    assert len(docs) == 2


def test_load_csv_empty_file(tmp_path, mongo_mock):
    handler = MongoHandler()
    handler.connect()

    csv_file = tmp_path / "empty.csv"
    pd.DataFrame(columns=["name"]).to_csv(csv_file, index=False)

    result = handler.load_csv("users", str(csv_file))
    assert result is None


def test_close(mongo_mock):
    handler = MongoHandler()
    handler.connect()
    handler.close()
    assert handler.client is not None  # mongomock client still exists
