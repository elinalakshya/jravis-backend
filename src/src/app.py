from fastapi import FastAPI

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
# FACTORY → PUBLISH PIPELINE
# -----------------------------

@app.post("/api/factory/generate")
def factory_generate_and_publish():
    try:
        print("🔥 FACTORY API TRIGGERED")

        product = generate_product()

        if not product:
            return {"status": "error", "msg": "No product generated"}

        # 🔧 ADAPTER (factory → engine)
        file_path = product.get("zip_path") or product.get("file_path")
        title = product.get("name") or product.get("title")

        if not file_path or not title:
            return {
                "status": "error",
                "msg": "Invalid product structure",
                "product": product,
            }

        print("📦 PRODUCT TITLE:", title)
        print("📄 PRODUCT FILE :", file_path)

        result = run_all_streams_micro_engine(
            zip_path=file_path,
            template_name=title,
            backend_url="api",
        )

        return {
            "status": "success",
            "product": title,
            "publish_result": result,
        }

    except Exception as e:
        print("❌ FACTORY ERROR:", e)
        return {"status": "error", "msg": str(e)}

