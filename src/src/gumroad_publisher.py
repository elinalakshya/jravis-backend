import requests
import os

GUMROAD_TOKEN = os.getenv("GUMROAD_TOKEN")
PRODUCT_ID = os.getenv("GUMROAD_PRODUCT_ID")


def publish_to_gumroad(title, description, price_rs, file_path):
    if not GUMROAD_TOKEN:
        raise Exception("❌ GUMROAD_TOKEN not set")
    if not PRODUCT_ID:
        raise Exception("❌ GUMROAD_PRODUCT_ID not set")

    # -----------------------------
    # UPDATE PRODUCT DETAILS (POST)
    # -----------------------------
    print("🟠 Updating Gumroad product details...")

    update_url = f"https://api.gumroad.com/v2/products/{PRODUCT_ID}.json"

    data = {
        "access_token": GUMROAD_TOKEN,
        "name": title,
        "price": int(price_rs * 100),  # INR → paise
        "description": description,
    }

    u = requests.post(update_url, data=data, timeout=60)

    print("🟠 Update status:", u.status_code)
    print("🟠 Update response FULL:")
    print(u.text)

    if u.status_code not in (200, 201):
        raise Exception("❌ Gumroad product update failed")

    # -----------------------------
    # UPLOAD FILE
    # -----------------------------
    print("📤 Uploading new file to Gumroad...")

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

    print("🚀 Gumroad product UPDATED successfully")
    return True

