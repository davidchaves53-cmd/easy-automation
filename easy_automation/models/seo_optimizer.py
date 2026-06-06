import os
import pandas as pd
from collections import Counter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

def load_latest_data(filename="merged_orders_listings.csv"):
    """
    Load merged dataset to extract titles, tags, and performance metrics.
    """
    path = os.path.join(PROCESSED_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Merged dataset not found: {path}")
    return pd.read_csv(path)

def extract_keywords(text):
    """
    Extract simple keywords from titles or tags.
    """
    if pd.isna(text):
        return []
    text = text.lower()
    for ch in [",", "|", "/", "-", "(", ")", ".", "!", "?"]:
        text = text.replace(ch, " ")
    words = [w.strip() for w in text.split() if len(w) > 2]
    return words

def build_keyword_scores(df):
    """
    Score keywords based on frequency and sales performance.
    """
    keyword_counter = Counter()
    keyword_sales = Counter()

    for _, row in df.iterrows():
        title_kw = extract_keywords(row.get("title", ""))
        tag_kw = extract_keywords(row.get("tags", ""))

        kws = title_kw + tag_kw

        for kw in kws:
            keyword_counter[kw] += 1
            keyword_sales[kw] += row.get("quantity", 0)

    keyword_df = pd.DataFrame({
        "keyword": list(keyword_counter.keys()),
        "frequency": list(keyword_counter.values()),
        "sales": [keyword_sales[k] for k in keyword_counter.keys()]
    })

    keyword_df["score"] = keyword_df["sales"] + keyword_df["frequency"] * 0.5
    keyword_df = keyword_df.sort_values("score", ascending=False)

    return keyword_df

def recommend_seo_for_listing(row, top_keywords):
    """
    Recommend SEO improvements for a single listing.
    """
    title_kw = set(extract_keywords(row.get("title", "")))
    tag_kw = set(extract_keywords(row.get("tags", "")))

    missing_keywords = []
    for kw in top_keywords:
        if kw not in title_kw and kw not in tag_kw:
            missing_keywords.append(kw)

    return missing_keywords[:5]  # top 5 suggestions

def generate_seo_recommendations():
    """
    Generate SEO suggestions for all listings.
    """
    print("Loading merged dataset...")
    df = load_latest_data()

    print("Building keyword scores...")
    keyword_df = build_keyword_scores(df)
    top_keywords = keyword_df["keyword"].head(50).tolist()

    print("Generating listing-level recommendations...")
    results = []

    for _, row in df.iterrows():
        listing_id = row["listing_id"]
        suggestions = recommend_seo_for_listing(row, top_keywords)

        results.append({
            "listing_id": listing_id,
            "current_title": row.get("title", ""),
            "current_tags": row.get("tags", ""),
            "recommended_keywords": ", ".join(suggestions)
        })

    out_path = os.path.join(PROCESSED_DIR, "seo_recommendations.csv")
    pd.DataFrame(results).to_csv(out_path, index=False)

    print(f"Saved SEO recommendations to: {out_path}")
    return out_path

if __name__ == "__main__":
    generate_seo_recommendations()
