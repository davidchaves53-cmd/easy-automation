import os
import pandas as pd
from etsy_actions import update_listing_price, update_listing_seo
from experiment_logger import log_change

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

def load_price_recs():
    path = os.path.join(PROCESSED_DIR, "price_recommendations.csv")
    if not os.path.exists(path):
        raise FileNotFoundError("price_recommendations.csv not found.")
    return pd.read_csv(path)

def load_seo_recs():
    path = os.path.join(PROCESSED_DIR, "seo_recommendations.csv")
    if not os.path.exists(path):
        raise FileNotFoundError("seo_recommendations.csv not found.")
    return pd.read_csv(path)

def apply_price_changes(dry_run=True):
    print("\n=== Applying Price Recommendations ===")
    df = load_price_recs()

    for _, row in df.iterrows():
        listing_id = row["listing_id"]
        current_price = row["current_price"]
        new_price = row["recommended_price"]

        if abs(new_price - current_price) < 0.10:
            continue  # ignore tiny changes

        print(f"Listing {listing_id}: {current_price} → {new_price}")

        if not dry_run:
            update_listing_price(listing_id, new_price)
            log_change(listing_id, "price_update", current_price, new_price)

def apply_seo_changes(dry_run=True):
    print("\n=== Applying SEO Recommendations ===")
    df = load_seo_recs()

    for _, row in df.iterrows():
        listing_id = row["listing_id"]
        suggestions = row["recommended_keywords"]

        if not suggestions or suggestions.strip() == "":
            continue

        new_tags = suggestions
        print(f"Listing {listing_id}: Adding SEO tags → {new_tags}")

        if not dry_run:
            update_listing_seo(listing_id, new_tags=new_tags)
            log_change(listing_id, "seo_update", "old_tags", new_tags)

def run_automation(dry_run=True):
    print("\n==============================")
    print(" RUNNING AUTOMATION ENGINE")
    print("==============================")

    apply_price_changes(dry_run=dry_run)
    apply_seo_changes(dry_run=dry_run)

    if dry_run:
        print("\nDry run complete. No real Etsy updates were made.")
    else:
        print("\nAutomation complete. Etsy listings updated.")

if __name__ == "__main__":
    run_automation(dry_run=True)
