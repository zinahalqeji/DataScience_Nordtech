"""
sentiment.py
--------------
Performs sentiment analysis on customer review text using a pre-trained BERT model.
"""

import pandas as pd
from transformers import pipeline


# Load sentiment analysis pipeline once (efficient for reuse)
sentiment_model = pipeline(
    "sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment"
)


def classify_sentiment(text: str) -> str:
    """
    Classify sentiment into Positive, Neutral, or Negative.
    """
    if not isinstance(text, str) or text.strip() == "":
        return "neutral"

    result = sentiment_model(text[:512])[0]["label"]

    if result in ["1 star", "2 stars"]:
        return "negative"
    elif result == "3 stars":
        return "neutral"
    else:
        return "positive"


def add_sentiment_column(df: pd.DataFrame, text_column: str) -> pd.DataFrame:
    """
    Apply sentiment classification to a DataFrame.
    """
    df["sentiment"] = df[text_column].apply(classify_sentiment)
    return df
