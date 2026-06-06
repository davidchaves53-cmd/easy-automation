import os
import pandas as pd
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "data", "processed")
DAILY_FILE = os.path.join(LOG_DIR, "daily_listing_data.csv")
LOG_FILE = os.path.join(LOG_DIR, "experiment_log.csv")

def load_daily_data():
    if not os.path.exists(DAILY_FILE):
        raise FileNotFoundError("daily_listing_data.csv not found.")
    return pd.read_csv(DAILY_FILE)

def init_log():
    if not os.path.exists(LOG_FILE):
        df = pd.DataFrame(columns=[
            "timestamp",
            "listing_id",
            "change_type",
            "old_value",
            "new_value"
        ])
        df.to_csv(LOG_FILE, index=False)

def log_change(listing_id, change_type, old_value, new_value):
    """
    Log any change: price, SEO, tags, title, etc.
    """
    init_log()
    df = pd.read_csv(LOG_FILE)

    new_row = {
        "timestamp": datetime.now().isoformat(),
        "listing_id": listing_id,
        "change_type": change_type,
        "old_value": old_value,
        "new_value": new_value
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(LOG_FILE, index=False)
    print(f"Logged change for listing {listing_id}")

def evaluate_change(listing_id, change_timestamp, window_days=7):
    """
    Compare performance before vs after a change.
    """
    df = load_daily_data()
    df["date"] = pd.to_datetime(df["date"])

    change_time = pd.to_datetime(change_timestamp)

    before_start = change_time - timedelta(days=window_days)
    before_end = change_time - timedelta(days=1)

    after_start = change_time + timedelta(days=1)
    after_end = change_time + timedelta(days=window_days)

    before = df[(df["listing_id"] == listing_id) &
                (df["date"] >= before_start) &
                (df["date"] <= before_end)]

    after = df[(df["listing_id"] == listing_id) &
               (df["date"] >= after_start) &
               (df["date"] <= after_end)]

    if before.empty or after.empty:
        return {"error": "Not enough data to evaluate change."}

    result = {
        "listing_id": listing_id,
        "before_units": before["units_sold"].sum(),
        "after_units": after["units_sold"].sum(),
        "before_revenue": before["revenue"].sum(),
        "after_revenue": after["revenue"].sum(),
        "units_change": after["units_sold"].sum() - before["units_sold"].sum(),
        "revenue_change": after["revenue"].sum() - before["revenue"].sum()
    }

    return result

def evaluate_all_changes():
    """
    Evaluate every logged change and produce a report.
    """
    init_log()
    log_df = pd.read_csv(LOG_FILE)

    results = []
    for _, row in log_df.iterrows():
        res = evaluate_change(row["listing_id"], row["timestamp"])
        if "error" not in res:
            res["change_type"] = row["change_type"]
            res["old_value"] = row["old_value"]
            res["new_value"] = row["new_value"]
            results.append(res)

    out_path = os.path.join(LOG_DIR, "experiment_results.csv")
    pd.DataFrame(results).to_csv(out_path, index=False)
    print(f"Saved experiment results to: {out_path}")
    return out_path

if __name__ == "__main__":
    evaluate_all_changes()
