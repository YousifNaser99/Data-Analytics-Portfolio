"""
profiler.py
-----------
Generate data quality profile
"""

import pandas as pd


class DataProfiler:

    @staticmethod
    def profile(df: pd.DataFrame):

        profile = {}

        profile["rows"] = len(df)
        profile["columns"] = len(df.columns)

        profile["missing_values"] = int(df.isna().sum().sum())

        profile["duplicate_rows"] = int(df.duplicated().sum())

        profile["memory_usage_mb"] = float(
        round(
             df.memory_usage(deep=True).sum() / 1024 / 1024,2
             )
         )

        profile["column_types"] = {
            col: str(dtype)
            for col, dtype in df.dtypes.items()
        }

        profile["unique_values"] = {
            col: int(df[col].nunique())
            for col in df.columns
        }

        profile["quality_score"] = round(
            (
                1
                - (
                    profile["missing_values"]
                    + profile["duplicate_rows"]
                )
                /
                max(len(df), 1)
            ) * 100,
            2,
        )

        return profile