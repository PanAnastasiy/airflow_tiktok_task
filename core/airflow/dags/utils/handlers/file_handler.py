import os


class FileHandler:
    """
    FileHandler provides static methods to perform basic file operations.
    """

    @staticmethod
    def is_empty(file_path: str) -> bool:
        """
        Check if a file is empty.

        Args:
            file_path (str): Path to the file.

        Returns:
            bool: True if the file is empty, False otherwise.
        """
        return os.path.getsize(file_path) == 0
