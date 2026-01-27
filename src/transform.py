import pandas as pd
import numpy as np


def clean_date(df):
    date_cols = ["orderdatum", "leveransdatum", "recensionsdatum"]

    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


def clean_prices(df):
    if "pris_per_enhet" not in df.columns:
        return df
    df["pris_per_enhet"] = (
        df["pris_per_enhet"]
        .astype(str)
        .str.replace(" ", "")
        .str.replace("SEK", "")
        .str.replace("kr", "")
        .str.replace(":-", "")
        .str.replace(",", ".")
    )
    df["pris_per_enhet"] = pd.to_numeric(df["pris_per_enhet"], errors="coerce")

    return df


def clean_region(df):
    mapping = {
        "sthlm": "stockholm",
        "sthml": "stockholm",
        "gothenburg": "göteborg",
        "gbgb": "göteborg",
        "gbg": "göteborg",
        "linkoping": "linköping",
        "malmo": "malmö",
        "orebro": "örebro",
        "vasteras": "västerås",
        "norr": "norrland",
        "nan": "unknown",
    }
    df["region"] = df["region"].astype(str).str.strip().str.lower().replace(mapping)

    return df


def clean_payment(df):
    mapping = {
        "kort": "card",
        "kreditkort": "card",
        "visa": "card",
        "mastercard": "card",
        "swish": "swish",
        "faktura": "invoice",
        "mobilbetalning": "swish",
    }

    df["betalmetod"] = (
        ["betalmetod"].astype(str).str.strip().str.lower().replace(mapping)
    )

    df["betalmetod"] = df["betalmetod"].fillna("unknown")
    return df
