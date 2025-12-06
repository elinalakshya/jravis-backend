# -----------------------------------------------------------
# JRAVIS — Payhip Auto Publisher
# Mission 2040 — Digital Marketplace Engine
# -----------------------------------------------------------

import os
import requests

PAYHIP_API_KEY = os.getenv("PAYHIP_API_KEY")
PAYHIP_EMAIL = os.getenv("PAYHIP_EMAIL")

BASE_URL = "https://payhip.com/api/v2"


# -----------------------------------------------------------
# Create Product
# -----------------------------------------------------------
def create_payhip_product(title, description, price):
    try:
        url = f"{BASE_URL}/products"

        payload = {
            "api_key": PAYHIP_API_KEY,
            "email": PAYHIP_EMAIL,
            "title": title,
            "description": description,
            "price": price,
            "type": "digital"
        }

        resp = requests.post(url, data=payload, timeout=20)
        data = resp.json()

        if not data.get("success"):
            print("[Payhip] ❌ Product creation failed:", data)
            return None

        return data["product"]["id"]

    except Exception as e:
        print("[Payhip] ❌ Error creating product:", e)
        return None


# -----------------------------------------------------------
# Upload digital file
# -----------------------------------------------------------
def upload_file(product_id, file_path):
    try:
        url = f"{BASE_URL}/products/{product_id}/files"

        files = {
            "file": (os.path.basename(file_path), open(file_path, "rb"))
        }

        payload = {
            "api_key": PAYHIP_API_KEY,
            "email": PAYHIP_EMAIL
        }

        resp = requests.post(url, data=payload, files=files, timeout=20)
        return resp.json()

    except Exception as e:
        print("[Payhip] ❌ Upload error:", e)
        return None


# -----------------------------------------------------------
# MAIN ENTRY — Called by Unified Engine
# -----------------------------------------------------------
def publish_to_payhip(template_name, zip_path):
    print(f"[Payhip] 🚀 Publishing {template_name} ...")

    if not PAYHIP_API_KEY:
        return {"status": "error", "message": "Missing PAYHIP_API_KEY"}

    # Step 1: Create product
    product_id = create_payhip_product(
        title=f"{template_name} — JRAVIS Template",
        description="Premium automated template by JRAVIS. Instant download.",
        price="12.00"
    )

    if not product_id:
        return {"status": "error", "message": "Payhip product creation failed"}

    # Step 2: Upload ZIP file
    upload_file(product_id, zip_path)

    product_url = f"https://payhip.com/{product_id}"

    print(f"[Payhip] ✅ Uploaded Successfully → {product_url}")

    return {
        "status": "success",
        "url": product_url,
        "product_id": product_id
    }
