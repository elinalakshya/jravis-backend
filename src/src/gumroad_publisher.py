import os
import json
import logging
import requests

from db import get_db

logging.basicConfig(level=logging.INFO)

GUMROAD_API_KEY = os.getenv("GUMROAD_API_KEY")
GUMROAD_CREATE_PRODUCT_URL = "https://api.gumroad.com/v2/products"


def publish_to_gumroad(product_id: str):
    if not GUMROAD_API_KEY:
        raise Exception("❌ GUMROAD_API_KEY not configured in environment")

    # -----------------------------
    # Load product from SQLite
    # -----------------------------
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT payload FROM products WHERE id=?", (product_id,))
    row = cur.fetchone()

    if not row:
        conn.close()
        raise Exception(f"❌ Product not found in DB: {product_id}")

    product = json.loads(row[0])

    title = product.get("title")
    description = product.get("description", "")
    price = int(product.get("price", 99))

    if not title:
        conn.close()
        raise Exception("❌ Product title missing")

    # -----------------------------
    # Prepare Gumroad Payload
    # -----------------------------
    payload = {
        "access_token": GUMROAD_API_KEY,
        "name": title,
        "description": description,
        "price": price * 100,   # Gumroad expects cents
        "currency": "USD",
        "published": True,
        "require_shipping": False,
    }

    logging.info(f"🚀 Publishing product to Gumroad: {title}")

    # -----------------------------
    # Send request to Gumroad
    # -----------------------------
    response = requests.post(
        GUMROAD_CREATE_PRODUCT_URL,
        data=payload,
        timeout=30
    )

    # -----------------------------
    # Handle Gumroad errors
    # -----------------------------
    if response.status_code != 200:
        logging.error(f"❌ Gumroad HTTP {response.status_code}: {response.text}")
        conn.close()
        raise Exception(
            f"Gumroad API error: status={response.status_code}, body={response.text}"
        )

    try:
        gumroad_response = response.json()
    except Exception:
        conn.close()
        raise Exception(
            f"Gumroad returned non-JSON response: {response.text}"
        )

    if not gumroad_response.get("success"):
        conn.close()
        raise Exception(
            f"Gumroad API failure: {gumroad_response}"
        )

    gumroad_product_id = gumroad_response["product"]["id"]

    # -----------------------------
    # Save Gumroad payload into DB
    # -----------------------------
    cur.execute(
        """
        UPDATE products
        SET gumroad_id = ?, gumroad_payload = ?
        WHERE id = ?
        """,
        (
            gumroad_product_id,
            json.dumps(gumroad_response),
            product_id
        )
    )

    conn.commit()
    conn.close()

    logging.info(f"✅ Published to Gumroad: {gumroad_product_id}")

    return {
        "product_id": product_id,
        "gumroad_product_id": gumroad_product_id,
        "status": "published"
    }

