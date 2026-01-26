import requests

GUMROAD_API = "https://api.gumroad.com/v2/products"

def create_gumroad_product(title, price_inr, description):
    data = {
        "access_token": GUMROAD_TOKEN,
        "name": title,
        "price": int(price_inr * 100),  # paise
        "description": description
    }
    r = requests.post(GUMROAD_API, data=data)
    r.raise_for_status()
    return r.json()["product"]["id"]


def upload_file(product_id, file_path):
    url = f"https://api.gumroad.com/v2/products/{product_id}/files"
    files = {"file": open(file_path, "rb")}
    data = {"access_token": GUMROAD_TOKEN}
    r = requests.post(url, data=data, files=files)
    r.raise_for_status()
