import os
import time
import requests
import logging
from db import get_db

GUMROAD_API_BASE = "https://api.gumroad.com/v2"


def get_access_token():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT access_token FROM gumroad_tokens ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    conn.close()

    if not row:
        raise Exception("❌ Gumroad not connected. Please run OAuth first.")

    return row[0]


def save_token(access_token, refresh_token=None, expires_in=None):
    expires_at = None
    if expires_in:
        expires_at = int(time.time()) + int(expires_in)

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO gumroad_tokens (access_token, refresh_token, expires_at) VALUES (?, ?, ?)",
        (access_token, refresh_token, expires_at),
    )
    conn.commit()
    conn.close()
    logging.info("✅ Gumroad token saved")


def publish_to_gumroad(product):
    token = get_access_token()

    payload = {
        "name": product["title"],
        "price": int(product["price"]) * 100,  # Gumroad uses cents
        "description": product["description"],
        "custom_permalink": product["sku"].lower(),
    }

    headers = {
        "Authorization": f"Bearer {token}"
    }

    r = requests.post(
        f"{GUMROAD_API_BASE}/products",
        data=payload,
        headers=headers,
        timeout=30
    )

    try:
        data = r.json()
    except Exception:
        raise Exception(f"Gumroad returned non-JSON response (status={r.status_code}): {r.text[:200]}")

    if not data.get("success"):
        raise Exception(f"Gumroad API error: {data}")

    return data["product"]

