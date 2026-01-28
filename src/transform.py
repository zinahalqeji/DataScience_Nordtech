import pandas as pd
import numpy as np


def clean_column_names(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df


def clean_id_columns(df):
    id_cols = ["order_id", "orderrad_id", "kund_id", "produkt_sku"]
    for col in id_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
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
        df["betalmetod"]
        .astype(str)
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
    df["betyg"] = df["betyg"].fillna(df["betyg"].median())

    return df


def remove_duplicates(df, unique_keys=None):
    # 1. Remove full-row duplicates
    df = df.drop_duplicates()

    # 2. If unique keys are provided, enforce uniqueness
    if unique_keys:
        df = df.drop_duplicates(subset=unique_keys, keep="first")

    return df

def fix_reversed_dates(df):
    if "orderdatum" not in df.columns or "leveransdatum" not in df.columns:
        return df
    order = df["orderdatum"]
    delivery = df["leveransdatum"]
    mask = delivery < order
    df.loc[mask, ["orderdatum", "leveransdatum"]] = df.loc[
        mask, ["leveransdatum", "orderdatum"]
    ].values
    return df


def clean_recension_text(df):
    if "recension_text" not in df.columns:
        return df

    # Convert to string and strip whitespace (safe even if no whitespace exists)
    col = df["recension_text"].astype(str).str.strip()

    # Replace placeholder strings with real NaN
    col = col.replace(
        ["nan", "none", "null", "na", ""], 
        np.nan
    )

    df["recension_text"] = col
    return df



def clean_all(df):
    df = clean_column_names(df)
    df = clean_id_columns(df)
    df = clean_date(df)
    df = fix_reversed_dates(df)
    df = clean_prices(df)
    df = clean_region(df)
    df = clean_payment(df)
    df = clean_antal(df)
    df = clean_kundtyp(df)
    df = clean_leveransstatus(df)
    df = clean_betyg(df)
    df = clean_recension_text(df)
    df = remove_duplicates(df)

    return df
