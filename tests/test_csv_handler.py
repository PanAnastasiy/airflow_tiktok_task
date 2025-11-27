import pandas as pd

from include.handlers.csv_handler import CSVHandler


def test_read_creates_dataframe(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("name,age\nAlice,30\nBob,25")

    df = CSVHandler.read(str(csv_file))
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 2)
    assert list(df.columns) == ["name", "age"]


def test_replace_nulls_replaces_nan():
    df = pd.DataFrame({"a": [1, None, 3], "b": [None, "x", None]})
    result = CSVHandler.replace_nulls(df)
    assert result.isnull().sum().sum() == 0
    assert (result == "-").sum().sum() >= 1


def test_sort_by_date_sorts_correctly():
    df = pd.DataFrame(
        {"created_date": ["2025-11-26", "2025-11-25", "2025-11-27"], "value": [1, 2, 3]}
    )
    sorted_df = CSVHandler.sort_by_date(df)
    dates = sorted_df["created_date"].tolist()
    assert dates == ["2025-11-25", "2025-11-26", "2025-11-27"]


def test_sort_by_date_no_column_returns_same():
    df = pd.DataFrame({"value": [3, 1, 2]})
    sorted_df = CSVHandler.sort_by_date(df)
    assert sorted_df.equals(df)


def test_clean_content_removes_unwanted_characters():
    df = pd.DataFrame({"content": ["Hello!@#", "Test123$", "Привет!"]})
    cleaned = CSVHandler.clean_content(df)
    assert all(c not in ["@", "#", "$"] for c in cleaned["content"].str.cat())
    assert "Hello" in cleaned["content"].iloc[0]
    assert "Привет" in cleaned["content"].iloc[2]


def test_save_creates_file(tmp_path):
    df = pd.DataFrame({"name": ["Alice", "Bob"], "age": [30, 25]})
    output_file = tmp_path / "output.csv"
    path = CSVHandler.save(df, str(output_file))
    assert path == str(output_file)
    read_df = pd.read_csv(output_file)
    assert read_df.equals(df)
