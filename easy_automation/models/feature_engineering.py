import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

def load_daily(filename="daily_listing_data.csv"):
    """
    Load the daily dataset created by daily_builder.py
    """
    path = os.path.join(PROCESSED_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Daily dataset not found: {path}")
    return pd.read_csv(path)

def add_date_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add day-of-week, month, and holiday flags.
    """
    df["date"] = pd.to_datetime(df["date"])
    df["dow"] = df["date"].dt.dayofweek
    df["month"] = df["date"].dt.month
    df["is_weekend"] = df["dow"].isin([5, 6]).astype(int)
    return df

def add_price_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add price-related features.
    """
    if "price_listing" in df.columns:
        df["price"] = df["price_listing"]
    elif "price" not in df.columns:
        df["price"] = 0  # fallback

    df["log_price"] = np.log1p(df["price"])
    return df

def add_seo_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add simple SEO features based on title and tags.
    """
    if "title" in df.columns:
        df["title_len"] = df["title"].astype(str).apply(len)
        df["title_word_count"] = df["title"].astype(str).apply(lambda x: len(x.split()))
    else:
        df["title_len"] = 0
        df["title_word_count"] = 0

    if "tags" in df.columns:
        df["num_tags"] = df["tags"].astype(str).apply(lambda x: len(x.split(",")))
    else:
        df["num_tags"] = 0

    return df

def add_lag_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add lagged features like yesterday's sales.
    """
    df = df.sort_values(["listing_id", "date"])
    df["units_sold_lag1"] = df.groupby("listing_id")["units_sold"].shift(1)
    df["revenue_lag1"] = df.groupby("listing_id")["revenue"].shift(1)

    df = df.fillna(0)
    return df

def save_training(df: pd.DataFrame, filename="training_data.csv"):
    """
    Save the final ML-ready dataset.
    """
    path = os.path.join(PROCESSED_DIR, filename)
    df.to_csv(path, index=False)
    print(f"Saved training dataset to: {path}")
    return path

if __name__ == "__main__":
    print("Loading daily dataset...")
    daily = load_daily()

    print("Adding features...")
    daily = add_date_features(daily)
    daily = add_price_features(daily)
    daily = add_seo_features(daily)
    daily = add_lag_features(daily)

    print("Saving training dataset...")
    save_training(daily)

    print("Done.")
