from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import requests

app = FastAPI()
    
@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"status": "JRAVIS API running"}

# -----------------------------
# CONFIG
# -----------------------------

GUMROAD_TOKEN = os.getenv("GUMROAD_TOKEN")

if not GUMROAD_TOKEN:
    print("⚠️ WARNING: GUMROAD_TOKEN not set in environment variables")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Example product folder
PRODUCT_FOLDER = os.path.join(BASE_DIR, "data", "products")

# -----------------------------
# MODELS
# -----------------------------

class GumroadProduct(BaseModel):
    title: str
    price: float   # in INR (e.g. 199)
    description: str
    filename: str  # only file name, not full path


# -----------------------------
# HEALTH CHECK
# -----------------------------

@app.get("/")
def health():
    return {"status": "JRAVIS running"}


# -----------------------------
# GUMROAD AUTO PUBLISH
# -----------------------------

@app.post("/api/gumroad/publish")
def publish_to_gumroad(product: GumroadProduct):

    if not GUMROAD_TOKEN:
        raise HTTPException(status_code=500, detail="GUMROAD_TOKEN missing")

    file_path = os.path.join(PRODUCT_FOLDER, product.filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File not found: {product.filename}")

    # -----------------
    # 1. CREATE PRODUCT
    # -----------------

    create_url = "https://api.gumroad.com/v2/products"

    create_data = {
        "access_token": GUMROAD_TOKEN,
        "name": product.title,
        "price": int(product.price * 100),  # paise
        "description": product.description
    }

    r = requests.post(create_url, data=create_data).json()

    if not r.get("success"):
        raise HTTPException(status_code=400, detail={"step": "create", "response": r})

    gumroad_product_id = r["product"]["id"]
    gumroad_url = r["product"]["short_url"]

    # -----------------
    # 2. UPLOAD FILE
    # -----------------

    upload_url = f"https://api.gumroad.com/v2/products/{gumroad_product_id}/files"

    with open(file_path, "rb") as f:
        files = {"file": f}
        upload_data = {"access_token": GUMROAD_TOKEN}
        u = requests.post(upload_url, files=files, data=upload_data).json()

    if not u.get("success"):
        raise HTTPException(status_code=400, detail={"step": "upload", "response": u})

    # -----------------
    # 3. PUBLISH PRODUCT
    # -----------------

    publish_url = f"https://api.gumroad.com/v2/products/{gumroad_product_id}"

    p = requests.put(publish_url, data={
        "access_token": GUMROAD_TOKEN,
        "published": True
    }).json()

    if not p.get("success"):
        raise HTTPException(status_code=400, detail={"step": "publish", "response": p})

    return {
        "status": "published",
        "product_id": gumroad_product_id,
        "url": gumroad_url
    }
