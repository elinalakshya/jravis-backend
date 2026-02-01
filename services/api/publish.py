from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
import requests
import os

router = APIRouter()

PRINTIFY_API_KEY = os.getenv("PRINTIFY_API_KEY")
SHOP_ID = os.getenv("PRINTIFY_SHOP_ID")
LOCK_CODE = os.getenv("LOCK_CODE", "Lock2040")


class PublishRequest(BaseModel):
    title: str
    description: str
    price: int
    design_image: str


def auth_lock(code: str):
    if code != LOCK_CODE:
        raise HTTPException(status_code=401, detail="Invalid lock code")


def create_printify_product(title, description, price, image_id):
    url = f"https://api.printify.com/v1/shops/{SHOP_ID}/products.json"

    payload = {
        "title": title,
        "description": description,
        "blueprint_id": 6,          # Unisex Heavy Cotton Tee
        "print_provider_id": 99,    # Printify Choice
        "variants": [
            {
                "id": 1,
                "price": price * 100,
                "is_enabled": True
            }
        ],
        "print_areas": [
            {
                "variant_ids": [1],
                "placeholders": [
                    {
                        "position": "front",
                        "images": [
                            {
                                "id": image_id,
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
        "Authorization": f"Bearer {PRINTIFY_API_KEY}",
        "Content-Type": "application/json"
    }

    r = requests.post(url, json=payload, headers=headers)

    if r.status_code not in (200, 201):
        raise HTTPException(status_code=500, detail=r.text)

    return r.json()


@router.post("/api/publish/draft_pod/{draft_id}")
def publish_pod(draft_id: str, body: PublishRequest, x_lock_code: str = Header(...)):
    auth_lock(x_lock_code)

    product = create_printify_product(
        body.title,
        body.description,
        body.price,
        body.design_image
    )

    return {"status": "success", "product": product}

