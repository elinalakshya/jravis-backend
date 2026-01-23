import os
import requests


GUMROAD_API_BASE = "https://api.gumroad.com/v2"


class GumroadPublisher:

    def __init__(self):
        self.token = os.getenv("GUMROAD_TOKEN")
        if not self.token:
            raise RuntimeError("GUMROAD_TOKEN not found in environment variables")

    # -----------------------------
    # CREATE PRODUCT
    # -----------------------------
    def create_product(self, title: str, price_rs: float, description: str):
        url = f"{GUMROAD_API_BASE}/products"

        data = {
            "access_token": self.token,
            "name": title,
            "price": int(price_rs * 100),  # INR → paise
            "description": description
        }

        r = requests.post(url, data=data, timeout=60).json()

        if not r.get("success"):
            raise Exception(f"Gumroad create failed: {r}")

        return {
            "id": r["product"]["id"],
            "url": r["product"]["short_url"]
        }

    # -----------------------------
    # UPLOAD FILE
    # -----------------------------
    def upload_file(self, product_id: str, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Product file not found: {file_path}")

        url = f"{GUMROAD_API_BASE}/products/{product_id}/files"

        with open(file_path, "rb") as f:
            files = {"file": f}
            data = {"access_token": self.token}
            r = requests.post(url, files=files, data=data, timeout=120).json()

        if not r.get("success"):
            raise Exception(f"Gumroad upload failed: {r}")

        return True

    # -----------------------------
    # PUBLISH PRODUCT
    # -----------------------------
    def publish_product(self, product_id: str):
        url = f"{GUMROAD_API_BASE}/products/{product_id}"

        data = {
            "access_token": self.token,
            "published": True
        }

        r = requests.put(url, data=data, timeout=60).json()

        if not r.get("success"):
            raise Exception(f"Gumroad publish failed: {r}")

        return True

    # -----------------------------
    # FULL PIPELINE
    # -----------------------------
    def publish_full(self, title: str, price_rs: float, description: str, file_path: str):
        product = self.create_product(title, price_rs, description)
        self.upload_file(product["id"], file_path)
        self.publish_product(product["id"])

        return {
            "status": "published",
            "product_id": product["id"],
            "url": product["url"]
        }
