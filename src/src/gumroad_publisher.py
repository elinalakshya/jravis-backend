# src/src/gumroad_publisher.py

import requests
import logging
from db import get_db
from gumroad_oauth import get_access_token

GUMROAD_PRODUCTS_API = "https://api.gumroad.com/v2/products"


def publish_product_to_gumroad(product_id: str):

    token = get_access_token()
    if not token:
        raise Exception("Gumroad not authenticated. Run OAuth first.")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT payload FROM products WHERE id = ?", (product_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        raise Exception("Product not found in DB")

    product = eval(row[0]) if isinstance(row[0], str) else row[0]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    data = {
        "name": product["title"],
        "price": product["price"],
        "description": product["description"],
    }

    r = requests.post(GUMROAD_PRODUCTS_API, headers=headers, data=data, timeout=60)

    if r.status_code != 200:
        raise Exception(f"Gumroad API error: {r.status_code} {r.text}")

    return r.json()
