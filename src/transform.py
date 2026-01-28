import pandas as pd
import numpy as np


def clean_column_names(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df


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
    }
    df["region"] = (
        df["region"]
        .astype(str)
        .str.strip()
        .str.lower()
        .replace("nan", None)
        .replace(mapping)
    )

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
        ["betalmetod"].astype(str)
        .str.strip()
        .str.lower()
        .replace("nan", None)
        .replace(mapping)
    )

    df["betalmetod"] = df["betalmetod"].fillna("unknown")
    return df


def clean_antal(df):
    word_map = {
        "en": 1,
        "ett": 1,
        "två": 2,
        "tva": 2,
        "tre": 3,
        "fyra": 4,
        "fem": 5,
        "sex": 6,
        "sju": 7,
        "åtta": 8,
        "nio": 9,
        "tio": 10,
    }

    # Step 1: convert to string
    col = df["antal"].astype(str).str.lower().str.strip()

    # Step 2: remove quotes
    col = col.str.replace('"', "", regex=False)

    # Step 3: remove "st" and spaces
    col = col.str.replace("st", "", regex=False).str.strip()

    # Step 4: replace Swedish words
    col = col.replace(word_map)

    # Step 5: convert to numeric
    df["antal"] = pd.to_numeric(col, errors="coerce")

    return df


def clean_kundtyp(df):
    col = df["kundtyp"].astype(str).str.strip().str.lower()

    mapping = {
        "privat": "private",
        "konsument": "private",
        "b2c": "private",
        "företag": "business",
        "firma": "business",
        "b2b": "business",
    }

    col = col.replace(mapping)

    df["kundtyp"] = col
    return df


def clean_leveransstatus(df):
    col = df["leveransstatus"].astype(str).str.strip().str.lower()

    mapping = {
        "levererad": "delivered",
        "mottagen": "received",
        "skickad": "sent",
        "under transport": "in_transit",
        "på väg": "in_transit",
        "pa väg": "in_transit",
        "pa vag": "in_transit",
        "retur": "returned",
        "returnerad": "returned",
        "återsänd": "returned",
        "atersand": "returned",
    }

    col = col.replace(mapping)

    # Replace string "nan" or empty with unknown
    col = col.replace(["nan", "none", ""], "unknown")

    df["leveransstatus"] = col
    return df


def clean_betyg(df):
    # Convert to numeric
    df["betyg"] = pd.to_numeric(df["betyg"], errors="coerce")

    # Clip invalid values
    df["betyg"] = df["betyg"].clip(lower=1, upper=5)

    # Fill missing with mean
    df["betyg"] = df["betyg"].fillna(df["betyg"].mean())

    return df
