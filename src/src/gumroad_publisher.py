import os
import requests
import logging
from db import get_db

GUMROAD_API_URL = "https://api.gumroad.com/v2/products"
GUMROAD_TOKEN = os.getenv("GUMROAD_API_TOKEN")

if not GUMROAD_TOKEN:
    logging.warning("⚠️ GUMROAD_API_TOKEN not set")


def publish_to_gumroad(product_id: str):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT payload FROM products WHERE id=?", (product_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        raise Exception("Product not found in DB")

    product = eval(row[0]) if isinstance(row[0], str) else row[0]

    headers = {
        "Authorization": f"Bearer {GUMROAD_TOKEN}"
    }

    payload = {
        "name": product["title"],
        "price": int(product["price"] * 100),  # Gumroad expects cents
        "description": product["description"],
        "published": True
    }

    response = requests.post(GUMROAD_API_URL, headers=headers, data=payload)

    if response.status_code != 200:
        raise Exception(
            f"Gumroad API error ({response.status_code}): {response.text}"
        )

    data = response.json()

    return {
        "gumroad_product_id": data["product"]["id"],
        "url": data["product"]["short_url"]
    }

