import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
MODELS_DIR = os.path.join(BASE_DIR, "models")

def load_training(filename="training_data.csv"):
    """
    Load the ML-ready dataset created by feature_engineering.py
    """
    path = os.path.join(PROCESSED_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Training dataset not found: {path}")
    return pd.read_csv(path)

def select_features(df: pd.DataFrame):
    """
    Select the features used for training.
    """
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

    X = df[feature_cols]
    y = df["units_sold"]

    return X, y, feature_cols

def train_model(X, y):
    """
    Train a RandomForestRegressor model.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=12,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    # Evaluate
    preds = model.predict(X_test)
    r2 = r2_score(y_test, preds)
    mae = mean_absolute_error(y_test, preds)

    print(f"Model R² Score: {r2:.4f}")
    print(f"Model MAE: {mae:.4f}")

    return model

def save_model(model, filename="demand_model.pkl"):
    """
    Save the trained model to /models/
    """
    os.makedirs(MODELS_DIR, exist_ok=True)
    path = os.path.join(MODELS_DIR, filename)
    joblib.dump(model, path)
    print(f"Saved model to: {path}")
    return path

if __name__ == "__main__":
    print("Loading training dataset...")
    df = load_training()

    print("Selecting features...")
    X, y, feature_cols = select_features(df)

    print("Training model...")
    model = train_model(X, y)

    print("Saving model...")
    save_model(model)

    print("Done.")
