import os
import requests
from experiment_logger import log_change

API_KEY = os.getenv("ETSY_API_KEY")
SHOP_ID = os.getenv("ETSY_SHOP_ID")
BASE_URL = "https://openapi.etsy.com/v3/application"
CLIENT_ID = "my_clent_id"
REDIRECT_URI = "my_redirect_url"
ACESS_TOKEN = "to_be_filled_after_oauth_flow"
REFRESH_TOKEN = "to_be_filled_after_oauth_flow"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

def update_listing_price(listing_id, new_price):
    """
    Update the price of a listing on Etsy.
    """
    url = f"{BASE_URL}/listings/{listing_id}"
    payload = {
        "price": float(new_price)
    }

    print(f"Updating price for listing {listing_id} → {new_price}")

    r = requests.patch(url, headers=HEADERS, json=payload)

    if r.status_code == 200:
        print("Price updated successfully.")
        log_change(listing_id, "price_update", "old_price", new_price)
    else:
        print("Error updating price:", r.text)

def update_listing_seo(listing_id, new_title=None, new_tags=None):
    """
    Update title and/or tags for a listing.
    """
    url = f"{BASE_URL}/listings/{listing_id}"
    payload = {}

    if new_title:
        payload["title"] = new_title
    if new_tags:
        payload["tags"] = new_tags.split(",")

    if not payload:
        print("No SEO fields provided.")
        return

    print(f"Updating SEO for listing {listing_id}")

    r = requests.patch(url, headers=HEADERS, json=payload)

    if r.status_code == 200:
        print("SEO updated successfully.")
        log_change(listing_id, "seo_update", "old_seo", payload)
    else:
        print("Error updating SEO:", r.text)
