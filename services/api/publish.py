import os
import requests
from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/publish", tags=["POD Publish"])


# =========================================================
# 🔐 LOCK SECURITY (Boss Protection)
# =========================================================
def verify_lock_code(x_lock_code: str = Header(None)):
    lock_code = os.getenv("LOCK_CODE")

    if not lock_code:
        raise HTTPException(status_code=500, detail="LOCK_CODE not set on server")

    if not x_lock_code:
        raise HTTPException(status_code=401, detail="Lock code missing")

    if x_lock_code.strip() != lock_code.strip():
        raise HTTPException(status_code=401, detail="Invalid lock code")


# =========================================================
# 📦 Request Model
# =========================================================
class PublishPayload(BaseModel):
    title: str
    description: str
    price: int
    design_image: str   # Printify uploaded image ID


# =========================================================
# 🚀 MAIN PUBLISH ROUTE
# =========================================================
@router.post("/draft_pod/{draft_id}")
def publish_product(
    draft_id: str,
    payload: PublishPayload,
    _: None = Depends(verify_lock_code)
):
    """
    Creates + publishes product directly to Printify shop
    """

    api_key = os.getenv("PRINTIFY_API_KEY")
    shop_id = os.getenv("PRINTIFY_SHOP_ID")

    if not api_key or not shop_id:
        raise HTTPException(status_code=500, detail="Printify env missing")

    # =====================================================
    # Product template (safe defaults)
    # Blueprint 6 = Unisex Heavy Cotton Tee
    # Provider 99 = Printify Choice
    # =====================================================
    product_body = {
        "title": payload.title,
        "description": payload.description,
        "blueprint_id": 6,
        "print_provider_id": 99,
        "variants": [
            {
                "id": 401,   # default variant
                "price": payload.price * 100,
                "is_enabled": True
            }
        ],
        "print_areas": [
            {
                "variant_ids": [401],
                "placeholders": [
                    {
                        "position": "front",
                        "images": [
                            {
                                "id": payload.design_image,
                                "x": 0.5,
                                "y": 0.5,
                                "scale": 1,
                                "angle": 0
                            }
                        ]
                    }
                ]
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # =====================================================
    # Step 1: Create product
    # =====================================================
    create = requests.post(
        f"https://api.printify.com/v1/shops/{shop_id}/products.json",
        json=product_body,
        headers=headers
    )

    if create.status_code != 201:
        raise HTTPException(
            status_code=500,
            detail=f"Printify create failed: {create.text}"
        )

    product_id = create.json()["id"]

    # =====================================================
    # Step 2: Publish product
    # =====================================================
    publish = requests.post(
        f"https://api.printify.com/v1/shops/{shop_id}/products/{product_id}/publish.json",
        headers=headers
    )

    if publish.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail=f"Publish failed: {publish.text}"
        )

    return {
        "status": "success",
        "product_id": product_id
    }

