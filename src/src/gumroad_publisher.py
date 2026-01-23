import os
import requests
from settings import GUMROAD_TOKEN


GUMROAD_API = "https://api.gumroad.com/v2"


def publish_to_gumroad(title: str, description: str, price_rs: int, file_path: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Gumroad file not found: {file_path}")

    # -----------------
    # CREATE PRODUCT
    # -----------------
    create_url = f"{GUMROAD_API}/products"

    data = {
        "access_token": GUMROAD_TOKEN,
        "name": title,
        "price": price_rs * 100,  # INR → paise
        "description": description
    }

    r = requests.post(create_url, data=data, timeout=60).json()

    if not r.get("success"):
        raise Exception(f"Gumroad create failed: {r}")

    product_id = r["product"]["id"]
    product_url = r["product"]["short_url"]

    print("🛒 Gumroad product created:", product_url)

    # -----------------
    # UPLOAD FILE
    # -----------------
    upload_url = f"{GUMROAD_API}/products/{product_id}/files"

    with open(file_path, "rb") as f:
        files = {"file": f}
        data = {"access_token": GUMROAD_TOKEN}
        u = requests.post(upload_url, files=files, data=data, timeout=120).json()

    if not u.get("success"):
        raise Exception(f"Gumroad upload failed: {u}")

    print("📤 Gumroad file uploaded")

    # -----------------
    # PUBLISH
    # -----------------
    pub_url = f"{GUMROAD_API}/products/{product_id}"

    p = requests.put(pub_url, data={
        "access_token": GUMROAD_TOKEN,
        "published": True
    }).json()

    if not p.get("success"):
        raise Exception(f"Gumroad publish failed: {p}")

    print("🚀 Gumroad product LIVE:", product_url)

    return product_url
