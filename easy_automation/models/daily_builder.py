import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

def load_merged(filename="merged_orders_listings.csv"):
    """
    Load the merged orders+listings file created by data_loader.py
    """
    path = os.path.join(PROCESSED_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Merged file not found: {path}")
    return pd.read_csv(path)

def build_daily_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert order-level data into daily listing-level aggregates.
    """
    # Ensure date column exists
    if "creation_tsz" in df.columns:
        df["date"] = pd.to_datetime(df["creation_tsz"], unit="s").dt.date
    elif "order_date" in df.columns:
        df["date"] = pd.to_datetime(df["order_date"]).dt.date
    else:
        raise KeyError("No usable date column found in merged dataset.")

    # Basic daily metrics
    daily = df.groupby(["listing_id", "date"]).agg(
        units_sold=("quantity", "sum"),
        revenue=("price_order", "sum"),
        num_orders=("order_id", "count")
    ).reset_index()

    # Fill missing values
    daily = daily.fillna(0)

    return daily

def save_daily(df: pd.DataFrame, filename="daily_listing_data.csv"):
    """
    Save daily dataset to data/processed.
    """
    path = os.path.join(PROCESSED_DIR, filename)
    df.to_csv(path, index=False)
    print(f"Saved daily dataset to: {path}")
    return path

if __name__ == "__main__":
    print("Loading merged dataset...")
    merged = load_merged()

    print("Building daily dataset...")
    daily = build_daily_dataset(merged)

    print("Saving daily dataset...")
    save_daily(daily)

    print("Done.")
