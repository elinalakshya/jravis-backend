import os
import json
import uuid
import logging
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
PRODUCT_DIR = os.path.join(DATA_DIR, "products")
LISTING_DIR = os.path.join(DATA_DIR, "listings")

os.makedirs(LISTING_DIR, exist_ok=True)

logging.basicConfig(level=logging.INFO)


# ---------------------------
# Helpers
# ---------------------------

def find_product(product_id: str):
    for folder in os.listdir(PRODUCT_DIR):
        meta_path = os.path.join(PRODUCT_DIR, folder, "product.json")
        if os.path.exists(meta_path):
            with open(meta_path) as f:
                meta = json.load(f)
                if meta["product_id"] == product_id:
                    return meta
    raise FileNotFoundError("Product not found")


# ---------------------------
# Listing Generator
# ---------------------------

def generate_listing_from_product(product_id: str):
    product = find_product(product_id)

    title = product["title"]

    bullets = [
        f"Instant digital download – no physical shipping",
        f"Designed for {product['type']} productivity and efficiency",
        f"Easy to customize and reuse",
        f"Perfect for freelancers, remote teams, entrepreneurs",
        f"Lifetime access after purchase"
    ]

    description = f"""
🚀 {title}

This professionally designed digital product helps you improve productivity, organization, and workflow efficiency.

✅ What you get:
- High quality digital file
- Ready-to-use format
- Fully editable
- Works on all devices

🎯 Best for:
- Entrepreneurs
- Remote workers
- Content creators
- Students
- Small teams

⚡ Instant download after purchase.
"""

    tags = [
        product["type"],
        "digital product",
        "planner",
        "productivity",
        "template",
        "instant download",
        "remote work",
        "business tools"
    ]

    price_map = {
        "excel": 7.99,
        "printable": 4.99,
        "canva": 9.99,
        "notion": 8.99,
        "generic": 5.99
    }

    price = price_map.get(product["type"], 5.99)

    listing_id = str(uuid.uuid4())

    listing = {
        "listing_id": listing_id,
        "product_id": product_id,
        "title": title,
        "price": price,
        "currency": "USD",
        "bullets": bullets,
        "description": description.strip(),
        "tags": tags,
        "created_at": datetime.utcnow().isoformat()
    }

    path = os.path.join(LISTING_DIR, f"{listing_id}.json")
    with open(path, "w") as f:
        json.dump(listing, f, indent=2)

    logging.info(f"🛒 Listing Generated | ID={listing_id} | Product={product_id}")
    logging.info(f"💾 Listing Saved → {path}")

    return listing
