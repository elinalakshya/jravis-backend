import os
import json
from fastapi import APIRouter, HTTPException, Depends

from services.printify_service import upload_image, create_product
from services.security import verify_lock_code

router = APIRouter()


def load_pod(product_id: str):
    path = f"data/listings_pod/{product_id}.json"
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        raise HTTPException(status_code=404, detail="POD JSON not found")


@router.post(
    "/api/publish/draft_pod/{product_id}",
    dependencies=[Depends(verify_lock_code)]
)
def draft_pod(product_id: str):

    p = load_pod(product_id)

    image_id = upload_image(p["design_image"])

    prod_id = create_product(
        title=p["title"],
        description=p["description"],
        blueprint_id=p["blueprint_id"],
        provider_id=p["print_provider_id"],
        image_id=image_id,
        variants=p["variants"],
        price=p["price"]
    )

    return {
        "status": "draft_created",
        "printify_product_id": prod_id,
        "product_id": product_id
    }


@router.post(
    "/api/publish/batch_pod",
    dependencies=[Depends(verify_lock_code)]
)
def batch_pod_upload():

    base = "data/listings_pod"
    results = []

    if not os.path.exists(base):
        raise HTTPException(status_code=500, detail="listings_pod folder missing")

    for fname in os.listdir(base):
        if not fname.endswith(".json"):
            continue

        path = os.path.join(base, fname)

        try:
            with open(path, "r", encoding="utf-8") as f:
                p = json.load(f)

            image_id = upload_image(p["design_image"])

            prod_id = create_product(
                title=p["title"],
                description=p["description"],
                blueprint_id=p["blueprint_id"],
                provider_id=p["print_provider_id"],
                image_id=image_id,
                variants=p["variants"],
                price=p["price"]
            )

            results.append({
                "file": fname,
                "status": "success",
                "printify_product_id": prod_id
            })

        except Exception as e:
            results.append({
                "file": fname,
                "status": "failed",
                "error": str(e)
            })

    return {
        "total": len(results),
        "results": results
    }
