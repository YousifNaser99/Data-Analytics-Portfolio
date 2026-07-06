"""
loader.py
----------
Responsible for loading datasets into a Pandas DataFrame.
Supported formats:
- Excel (.xlsx, .xls)
- CSV (.csv)
"""

from pathlib import Path
import pandas as pd


class DataLoader:
    """Load datasets from supported file formats."""

    SUPPORTED_EXTENSIONS = [".xlsx", ".xls", ".csv"]

    @staticmethod
    def load(file_path: str) -> pd.DataFrame:
        """
        Load dataset from Excel or CSV.

        Args:
            file_path (str): Path to input dataset.

        Returns:
            pd.DataFrame
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        extension = path.suffix.lower()

        if extension not in DataLoader.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file format: {extension}"
            )

        if extension == ".csv":
            return pd.read_csv(path)

        return pd.read_excel(path)