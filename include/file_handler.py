import os

import pandas as pd


class FileHandler:
    @staticmethod
    def is_empty(file_path: str) -> bool:
        return os.path.getsize(file_path) == 0


