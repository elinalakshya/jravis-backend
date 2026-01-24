import requests
import os

GUMROAD_TOKEN = os.getenv("GUMROAD_TOKEN")
PRODUCT_ID = os.getenv("GUMROAD_PRODUCT_ID")


def publish_to_gumroad(title, description, price_rs, file_path):
    if not GUMROAD_TOKEN:
        raise Exception("❌ GUMROAD_TOKEN not set")
    if not PRODUCT_ID:
        raise Exception("❌ GUMROAD_PRODUCT_ID not set")

    print("📤 Uploading new file to Gumroad product shell...")

    upload_url = f"https://api.gumroad.com/v2/products/{PRODUCT_ID}/files.json"

    with open(file_path, "rb") as f:
        upload = requests.post(
            upload_url,
            data={"access_token": GUMROAD_TOKEN},
            files={"file": f},
            timeout=120,
        )

    print("📤 Upload status:", upload.status_code)
    print("📤 Upload response FULL:")
    print(upload.text)

    try:
        up = upload.json()
    except Exception:
        raise Exception("❌ Gumroad upload did not return JSON")

    if not up.get("success"):
        raise Exception(f"❌ Gumroad upload failed: {up}")

    print("🚀 Gumroad file uploaded successfully")
    return True

