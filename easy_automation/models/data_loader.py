import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

def load_orders(filename: str) -> pd.DataFrame:
    """
    Load raw Etsy orders CSV from data/raw.
    Example filename: 'orders_2024.csv'
    """
    path = os.path.join(RAW_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Orders file not found: {path}")
    df = pd.read_csv(path)
    return df

def load_listings(filename: str) -> pd.DataFrame:
    """
    Load raw Etsy listings CSV from data/raw.
    Example filename: 'listings_export.csv'
    """
    path = os.path.join(RAW_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Listings file not found: {path}")
    df = pd.read_csv(path)
    return df

def merge_orders_listings(orders_df: pd.DataFrame, listings_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge orders with listings on listing_id (or equivalent column).
    You may need to adjust column names to match your actual exports.
    """
    # Guessing common column names – adjust if your CSVs differ
    if "listing_id" not in orders_df.columns:
        raise KeyError("orders_df must contain 'listing_id' column")
    if "listing_id" not in listings_df.columns:
        raise KeyError("listings_df must contain 'listing_id' column")

    merged = orders_df.merge(listings_df, on="listing_id", how="left", suffixes=("_order", "_listing"))
    return merged

def save_processed(df: pd.DataFrame, filename: str) -> str:
    """
    Save a processed dataframe to data/processed.
    """
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    path = os.path.join(PROCESSED_DIR, filename)
    df.to_csv(path, index=False)
    print(f"Saved processed file to: {path}")
    return path

if __name__ == "__main__":
    # Example usage – update filenames to match your actual exports
    orders_file = "orders_2024.csv"
    listings_file = "listings_export.csv"

    print("Loading raw data...")
    orders = load_orders(orders_file)
    listings = load_listings(listings_file)

    print("Merging orders and listings...")
    merged = merge_orders_listings(orders, listings)

    print("Saving merged data...")
    save_processed(merged, "merged_orders_listings.csv")

    print("Done.")
