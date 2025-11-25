import os

import pandas as pd
from airflow.sdk import task, task_group

from include.consts import PROCESSED_PATH
from include.handlers.csv_handler import CSVHandler
from include.handlers.file_handler import FileHandler


@task.branch
def check_file_empty(file_path: str) -> str:
    """
    Branching task to check if a file is empty.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: Task ID to follow based on file emptiness.
    """
    if FileHandler.is_empty(file_path):
        return "file_is_empty"
    return "extract_data"


@task.bash
def file_is_empty() -> str:
    """
    Task executed when the file is empty.

    Returns:
        str: Bash command output.
    """
    return 'echo "File is empty. DAG terminated."'  # Message in English


# -------------------- Processing --------------------
@task
def extract_data(file_path: str) -> pd.DataFrame:
    """
    Extract CSV data into a pandas DataFrame.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    return CSVHandler.read(file_path)


@task_group
def transform_group(df: pd.DataFrame) -> pd.DataFrame:
    """
    Task group for transforming and cleaning the DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Transformed and cleaned DataFrame.
    """

    @task
    def replace_nulls(df: pd.DataFrame) -> pd.DataFrame:
        return CSVHandler.replace_nulls(df)

    @task
    def sort_data(df: pd.DataFrame) -> pd.DataFrame:
        return CSVHandler.sort_by_date(df)

    @task
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        return CSVHandler.clean_content(df)

    step1 = replace_nulls(df)
    step2 = sort_data(step1)
    cleaned = clean_data(step2)
    return cleaned


@task
def load_data(df: pd.DataFrame, file_path: str) -> str:
    """
    Save the transformed DataFrame to a processed CSV file.

    Args:
        df (pd.DataFrame): DataFrame to save.
        file_path (str): Original CSV file path.

    Returns:
        str: Path to the saved processed CSV file.
    """
    file_name = os.path.basename(file_path).replace(".csv", "")
    output_path = os.path.join(PROCESSED_PATH, f"{file_name}_processed.csv")
    CSVHandler.save(df, output_path)
    return output_path
