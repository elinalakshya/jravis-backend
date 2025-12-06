# -----------------------------------------------------------
# GUMROAD PUBLISHER — JRAVIS Phase-1 Monetization System
# -----------------------------------------------------------

import os
import requests

GUMROAD_TOKEN = os.getenv("GUMROAD_API_KEY", "")

def upload_to_gumroad(zip_path: str, title: str):
    """
    Uploads a product ZIP to Gumroad.
    JRAVIS uses this for template marketplaces.
    """

    print(f"[GUMROAD] Uploading {title}...")

    if not GUMROAD_TOKEN:
        print("[GUMROAD] ❌ Missing API Key")
        return {"status": "error", "reason": "missing_api_key"}

    try:
        url = "https://api.gumroad.com/v2/products"

        files = {"content": open(zip_path, "rb")}

        data = {
            "name": title,
            "price": 500,  # ₹500 ~ $6
            "published": "true"
        }

        r = requests.post(url, data=data, files=files, params={"access_token": GUMROAD_TOKEN})
        print("[GUMROAD] Response:", r.json())

        return {"status": "ok", "response": r.json()}

    except Exception as e:
        print("[GUMROAD] ERROR:", e)
        return {"status": "error", "reason": str(e)}
