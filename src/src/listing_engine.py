import os
import json
from typing import Dict, Any

# ---------------------------------------------------------
# Resolve project root safely (works locally + Render)
# ---------------------------------------------------------

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# src/src → project root
PROJECT_ROOT = os.path.abspath(
    os.path.join(CURRENT_DIR, "..", "..")
)

DATA_DIR = os.path.join(PROJECT_ROOT, "data")
PRODUCT_DIR = os.path.join(DATA_DIR, "products")

print("✅ PROJECT_ROOT:", PROJECT_ROOT)
print("✅ PRODUCT_DIR:", PRODUCT_DIR)
print("📂 PRODUCT_DIR exists:", os.path.exists(PRODUCT_DIR))


def find_product(product_id: str) -> Dict[str, Any]:
    """
    Locate and load a product JSON file by product_id.
    Supports:
    - Direct filename match: <product_id>.json
    - Fallback scan inside all JSON files
    """

    if not os.path.exists(PRODUCT_DIR):
        raise FileNotFoundError(f"PRODUCT_DIR not found: {PRODUCT_DIR}")

    print("🔍 Searching product_id:", product_id)
    print("📂 Files in PRODUCT_DIR:", os.listdir(PRODUCT_DIR))

    # -------------------------------------------------
    # ✅ FAST PATH — direct filename match
    # -------------------------------------------------
    direct_file = os.path.join(PRODUCT_DIR, f"{product_id}.json")

    if os.path.exists(direct_file):
        print("✅ Direct product file found:", direct_file)
        with open(direct_file, "r", encoding="utf-8") as f:
            return json.load(f)

    # -------------------------------------------------
    # 🔁 FALLBACK — scan all JSON files
    # -------------------------------------------------
    for filename in os.listdir(PRODUCT_DIR):
        if not filename.endswith(".json"):
            continue

        file_path = os.path.join(PRODUCT_DIR, filename)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                product = json.load(f)

            # Try multiple possible keys safely
            pid = (
                product.get("product_id")
                or product.get("id")
                or product.get("uuid")
            )

            if pid == product_id:
                print(f"✅ Product matched inside file: {file_path}")
                return product

        except Exception as e:
            print(f"⚠️ Failed reading product file {filename}: {e}")

    # -------------------------------------------------
    # ❌ Not found
    # -------------------------------------------------
    raise ValueError(f"❌ Product not found for product_id: {product_id}")


# ---------------------------------------------------------
# Listing Generator
# ---------------------------------------------------------

def generate_listing_from_product(product_id: str) -> Dict[str, Any]:
    """
    Generate marketplace listing payload from product JSON.
    """

    product = find_product(product_id)

    title = product.get("title", "").strip()
    description = product.get("description", "").strip()
    price = product.get("price", 0)
    tags = product.get("tags", [])
    sku = product.get("sku")

    if not title:
        raise ValueError("Product title missing")

    listing = {
        "product_id": product_id,
        "sku": sku,
        "title": title,
        "description": description,
        "price": price,
        "tags": tags,
        "status": "ready",
    }

    print("🚀 Listing generated successfully")
    return listing
