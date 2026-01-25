from fastapi import FastAPI
import os
import traceback

from product_factory import generate_product
from unified_engine import run_all_streams_micro_engine

app = FastAPI()


# -----------------------------
# HEALTH
# -----------------------------
@app.get("/")
def root():
    return {"status": "JRAVIS API running"}


@app.get("/healthz")
def health():
    return {"ok": True}


# -----------------------------
# FACTORY → PUBLISH PIPELINE
# -----------------------------
@app.post("/api/factory/generate")
def factory_generate():

    print("🔥 FACTORY API TRIGGERED")

    try:
        # 1. CREATE PRODUCT
        product = generate_product()

        if not product or "file_path" not in product:
            return {
                "status": "error",
                "msg": "Invalid product structure",
                "product": product,
            }

        print("📄 PRODUCT FILE :", product["file_path"])
        print("📦 PRODUCT TITLE:", product["title"])
        print("💰 PRICE        :", product["price"])

        # 2. PUBLISH
        publish_result = run_all_streams_micro_engine(
            title=product["title"],
            description=product["description"],
            price=product["price"],
            zip_path=product["file_path"],   # ✅ FIXED (was file_path earlier)
        )

        return {
            "status": "success",
            "product": product["title"],
            "publish_result": publish_result,
        }

    except Exception as e:
        print("❌ FACTORY ERROR:", e)
        traceback.print_exc()

        return {
            "status": "error",
            "msg": str(e),
        }
