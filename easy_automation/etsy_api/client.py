import requests
import os

API_KEY = os.getenv("ETSY_API_KEY")
SHOP_ID = os.getenv("ETSY_SHOP_ID")
BASE_URL = "https://openapi.etsy.com/v3/application"

def get_listings():
    url = f"{BASE_URL}/shops/{SHOP_ID}/listings/active"
    headers = {"x-api-key": API_KEY}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()

def get_receipts(limit=100):
    url = f"{BASE_URL}/shops/{SHOP_ID}/receipts"
    headers = {"x-api-key": API_KEY}
    params = {"limit": limit}
    r = requests.get(url, headers=headers, params=params)
    r.raise_for_status()
    return r.json()