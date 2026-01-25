from fastapi import FastAPI
import os

# JRAVIS engines
from product_factory import generate_product
from unified_engine import run_all_streams_micro_engine

app = FastAPI()


# -----------------------------
# HEALTH
# -----------------------------

@app.get("/")
def root():
    return {"status": "JRAVIS running"}

@app.get("/healthz")
def health():
    return {"status": "ok"}


# -----------------------------
# FACTORY + AUTO PUBLISH
# -----------------------------

@app.post("/api/factory/generate")
def factory_generate_and_publish():
    try:
        print("🔥 FACTORY API TRIGGERED")

        product = generate_product()

        if not product:
            return {"status": "error", "msg": "No product generated"}

        if "file_path" not in product or "title" not in product:
            return {"status": "error", "msg": "Invalid product structure", "product": product}

        print("📦 PRODUCT TITLE:", product["title"])
        print("📄 PRODUCT FILE :", product["file_path"])

        result = run_all_streams_micro_engine(
            zip_path=product["file_path"],
            template_name=product["title"],
            backend_url="api",
        )

        return {
            "status": "success",
            "product": product["title"],
            "publish_result": result,
        }

    except Exception as e:
        print("❌ FACTORY ERROR:", e)
        return {"status": "error", "msg": str(e)}

