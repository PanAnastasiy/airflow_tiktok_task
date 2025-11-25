import re

import pandas as pd


class CSVHandler:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = pd.read_csv(file_path)

    def replace_nulls(self):
        self.df.fillna("-", inplace=True)
        return self

    def sort_by_date(self):
        if "created_date" in self.df.columns:
            self.df = self.df.sort_values("created_date")
        return self

    def clean_content(self):
        self.df["content"] = self.df["content"].apply(
            lambda text: re.sub(r"[^а-яА-Яa-zA-Z0-9 .,!?:;\"'-]", "", str(text))
        )
        return self

    def save(self, output_path: str):
        self.df.to_csv(output_path, index=False)
        return output_path