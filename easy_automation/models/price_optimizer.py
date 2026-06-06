import os
import numpy as np
import pandas as pd
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
MODELS_DIR = os.path.join(BASE_DIR, "models")

def load_model(filename="demand_model.pkl"):
    """
    Load the trained demand model.
    """
    path = os.path.join(MODELS_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model not found: {path}")
    return joblib.load(path)

def load_latest_data(filename="training_data.csv"):
    """
    Load the latest feature-engineered dataset.
    """
    path = os.path.join(PROCESSED_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Training data not found: {path}")
    return pd.read_csv(path)

def suggest_price_for_listing(row, model, feature_cols, fee_rate=0.08, cost=0):
    """
    Suggest the best price for a single listing.
    """
    current_price = row["price"]
    candidates = np.linspace(current_price * 0.8, current_price * 1.2, 9)

    best_price = current_price
    best_profit = -1e9

    base_features = row[feature_cols].copy()

    for p in candidates:
        base_features["price"] = p
        base_features["log_price"] = np.log1p(p)

        pred_units = model.predict([base_features.values])[0]
        profit = (p * (1 - fee_rate) - cost) * pred_units

        if profit > best_profit:
            best_profit = profit
            best_price = p

    return best_price, best_profit

def generate_price_recommendations():
    """
    Generate price suggestions for all listings.
    """
    print("Loading model...")
    model = load_model()

    print("Loading latest data...")
    df = load_latest_data()

    feature_cols = [
        "price",
        "log_price",
        "dow",
        "month",
        "is_weekend",
        "title_len",
        "title_word_count",
        "num_tags",
        "units_sold_lag1",
        "revenue_lag1"
    ]

    print("Generating recommendations...")
    results = []

    for _, row in df.iterrows():
        listing_id = row["listing_id"]
        best_price, best_profit = suggest_price_for_listing(row, model, feature_cols)
        results.append({
            "listing_id": listing_id,
            "current_price": row["price"],
            "recommended_price": round(best_price, 2),
            "expected_profit": round(best_profit, 2)
        })

    results_df = pd.DataFrame(results)
    out_path = os.path.join(PROCESSED_DIR, "price_recommendations.csv")
    results_df.to_csv(out_path, index=False)

    print(f"Saved price recommendations to: {out_path}")
    return results_df

if __name__ == "__main__":
    generate_price_recommendations()
