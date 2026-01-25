from fastapi import FastAPI
from product_factory import generate_product
from unified_engine import run_all_streams_micro_engine

app = FastAPI()


@app.get("/")
def root():
    return {"status": "JRAVIS API running"}


@app.get("/healthz")
def health():
    return {"ok": True}


@app.post("/api/factory/generate")
def factory_generate():
    try:
        print("🔥 FACTORY API TRIGGERED")

        product = generate_product()

        run_all_streams_micro_engine(
            file_path=product["file_path"],
            title=product["title"],
            description=product["description"],
            price=product["price"],
        )

        return {
            "status": "success",
            "product": product["title"],
            "download_path": product["file_path"],
        }

    except Exception as e:
        print("❌ FACTORY ERROR:", e)
        return {"status": "error", "msg": str(e)}
