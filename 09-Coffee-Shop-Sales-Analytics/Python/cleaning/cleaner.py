"""
cleaner.py
----------
Data Cleaning Engine
"""

import pandas as pd


class DataCleaner:

    @staticmethod
    def clean(df: pd.DataFrame):

        report = {}

        # ==============================
        # Before Cleaning
        # ==============================
        report["rows_before"] = len(df)
        report["columns"] = len(df.columns)

        # ==============================
        # Clean Column Names
        # ==============================
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        # ==============================
        # Remove Empty Rows Only
        # ==============================
        before = len(df)
        df = df.dropna(how="all")
        report["empty_rows_removed"] = before - len(df)

        # ==============================
        # Remove Duplicate Rows
        # ==============================
        before = len(df)
        df = df.drop_duplicates()
        report["duplicates_removed"] = before - len(df)

        # ==============================
        # Clean Text Columns
        # ==============================
        text_columns = df.select_dtypes(include="object").columns

        for col in text_columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.replace(r"\s+", " ", regex=True)
            )

        # ==============================
        # Missing Values
        # ==============================
        report["missing_values"] = df.isna().sum().to_dict()

        # ==============================
        # After Cleaning
        # ==============================
        report["rows_after"] = len(df)

        return df, report