import pandas as pd
from pathlib import Path


def load_csv(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path)
        print(f"Data loaded successfully from {file_path}")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")


def initial_eda(df: pd.DataFrame) -> None:
    print("\n--- BASIC INFO ---")
    print(df.info())

    print("\n--- DESCRIBE (NUMERIC) ---")
    print(df.describe())

    print("\n--- MISSING VALUES ---")
    print(df.isna().sum())

    print("\n--- SAMPLE ROWS ---")
    print(df.head())


if __name__ == "__main__":
    RAW_DATA_PATH = Path("data/raw/nordtech_data.csv")
    df_raw = load_csv(RAW_DATA_PATH)
    initial_eda(df_raw)
