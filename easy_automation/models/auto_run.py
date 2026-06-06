import os
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))

ORDERS_PATH = os.path.join(BASE, "orders_2024.csv")
LISTINGS_PATH = os.path.join(BASE, "listings_export.csv")
OUTPUT_PATH = os.path.join(BASE, "daily_output.csv")

def load_csv(path):
    return pd.read_csv(path)

def merge():
    orders = load_csv(ORDERS_PATH)
    listings = load_csv(LISTINGS_PATH)
    merged = orders.merge(listings, on="SKU", how="left")
    merged.to_csv(OUTPUT_PATH, index=False)

if __name__ == "__main__":
    merge()
