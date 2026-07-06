from sqlalchemy import text
from sql_loader import SQLLoader

engine = SQLLoader.get_engine()

with engine.connect() as conn:
    result = conn.execute(text("SELECT @@VERSION"))

    print("=" * 60)
    print("CONNECTED SUCCESSFULLY")
    print("=" * 60)

    print(result.fetchone()[0])