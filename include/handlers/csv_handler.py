import re

import pandas as pd


class CSVHandler:
    """
    CSVHandler provides static methods for reading, cleaning, transforming,
    and saving CSV data using pandas DataFrames.
    """

    @staticmethod
    def read(file_path: str) -> pd.DataFrame:
        """
        Read a CSV file into a pandas DataFrame.

        Args:
            file_path (str): Path to the CSV file.

        Returns:
            pd.DataFrame: Loaded DataFrame with all columns as strings.
        """
        return pd.read_csv(
            file_path,
            on_bad_lines="skip",
            dtype=str,
            encoding="utf-8",
        )

    @staticmethod
    def replace_nulls(df: pd.DataFrame) -> pd.DataFrame:
        """
        Replace all NaN/null values in the DataFrame with a dash ("-").

        Args:
            df (pd.DataFrame): Input DataFrame.

        Returns:
            pd.DataFrame: DataFrame with nulls replaced.
        """
        return df.fillna("-")

    @staticmethod
    def sort_by_date(df: pd.DataFrame) -> pd.DataFrame:
        """
        Sort the DataFrame by the 'created_date' column if it exists.

        Args:
            df (pd.DataFrame): Input DataFrame.

        Returns:
            pd.DataFrame: Sorted DataFrame.
        """
        if "created_date" in df.columns:
            return df.sort_values("created_date")
        return df

    @staticmethod
    def clean_content(df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the 'content' column by removing unwanted characters.
        Keeps only letters, numbers, spaces, and common punctuation.

        Args:
            df (pd.DataFrame): Input DataFrame.

        Returns:
            pd.DataFrame: DataFrame with cleaned 'content' column.
        """
        if "content" in df.columns:
            df["content"] = df["content"].apply(
                lambda text: re.sub(r"[^а-яА-Яa-zA-Z0-9 .,!?:;\"'-]", "", str(text))
            )
        return df

    @staticmethod
    def save(df: pd.DataFrame, output_path: str) -> str:
        """
        Save the DataFrame to a CSV file.

        Args:
            df (pd.DataFrame): DataFrame to save.
            output_path (str): Output CSV file path.

        Returns:
            str: The path to the saved CSV file.
        """
        df.to_csv(output_path, index=False)
        return output_path
