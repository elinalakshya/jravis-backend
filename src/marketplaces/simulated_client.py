# -----------------------------------------------------------
# Simulated Marketplace Client — Batch 10
# Creates cloud URLs for every marketplace upload
# -----------------------------------------------------------

import random

BASE_URL = "https://jravis.cloud"

MARKETPLACES = [
    "gumroad",
    "payhip",
    "etsy",
    "shopify",
    "creative-market",
    "webflow",
    "notion",
]

def upload_to_marketplace(template_name: str):
    """
    Simulates an upload by generating a JRAVIS Cloud URL.
    No real API keys required.
    """
    marketplace = random.choice(MARKETPLACES)
    url = f"{BASE_URL}/{marketplace}/{template_name}"

    return {
        "marketplace": marketplace,
        "url": url,
        "status": "uploaded"
    }

def upload_to_all(template_name: str):
    """
    Uploads to every marketplace (simulated).
    """
    results = []
    for m in MARKETPLACES:
        url = f"{BASE_URL}/{m}/{template_name}"
        results.append({"marketplace": m, "url": url, "status": "uploaded"})

    return {
        "template": template_name,
        "uploaded_to": results
    }
