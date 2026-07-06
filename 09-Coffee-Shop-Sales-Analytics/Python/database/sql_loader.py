"""
sql_loader.py
-------------
Load Pandas DataFrame into SQL Server.
"""

from urllib.parse import quote_plus

import pandas as pd
from sqlalchemy import create_engine


print(">>> SQL LOADER MODULE LOADED")


class SQLLoader:

    SERVER = r"localhost\SQLEXPRESS"
    DATABASE = "AI_Data_Analysis_Platform"

    @classmethod
    def get_engine(cls):

        connection_string = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"SERVER={cls.SERVER};"
            f"DATABASE={cls.DATABASE};"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )

        engine = create_engine(
            "mssql+pyodbc:///?odbc_connect=%s"
            % quote_plus(connection_string),
            fast_executemany=True,
        )

        return engine

    @classmethod
    def load_dataframe(
        cls,
        df: pd.DataFrame,
        table_name: str,
    ):

        print("=" * 60)
        print("SQL LOADER STARTED")
        print("=" * 60)

        print(f"Table : {table_name}")
        print(f"Rows  : {len(df)}")

        engine = cls.get_engine()
        from sqlalchemy import text

        with engine.begin() as conn:
         conn.execute(text(f"TRUNCATE TABLE {table_name}"))

        try:

            df.to_sql(
                name=table_name,
                con=engine,
                if_exists="append",
                index=False,
                chunksize=5000,
            )

            print(">>> INSERT SUCCESSFUL")

        except Exception as e:

            print(">>> INSERT FAILED")
            print(e)
            raise

        finally:

            engine.dispose()

            print(">>> CONNECTION CLOSED")