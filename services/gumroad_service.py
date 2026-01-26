import os
import requests

GUMROAD_TOKEN = os.getenv("GUMROAD_TOKEN")


def create_product(title, price_inr, description):
    url = "https://api.gumroad.com/v2/products"
    data = {
        "access_token": GUMROAD_TOKEN,
        "name": title,
        "price": int(price_inr * 100),  # paise
        "description": description,
        "published": False
    }
    r = requests.post(url, data=data, timeout=60)
    r.raise_for_status()
    return r.json()["product"]["id"]


def upload_file(product_id, file_path):
    url = f"https://api.gumroad.com/v2/products/{product_id}/files"
    data = {"access_token": GUMROAD_TOKEN}
    with open(file_path, "rb") as f:
        files = {"file": f}
        r = requests.post(url, data=data, files=files, timeout=120)
        r.raise_for_status()
