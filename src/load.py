import sqlite3
import pandas as pd
from pathlib import Path


def load_to_sqlite(
    df: pd.DataFrame,
    db_path: str,
    table_name: str = "clean_orders",
    if_exists: str = "replace",
) -> None:
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)

    try:
        df.to_sql(table_name, conn, if_exists=if_exists, index=False)
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]
        print(f"Loaded {row_count} rows into table '{table_name}'.")
    finally:
        conn.close()
