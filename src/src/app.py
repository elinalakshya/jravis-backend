# src/src/app.py

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
    print("🔥 FACTORY API TRIGGERED")

    product = generate_product()

    result = run_all_streams_micro_engine(
        file_path=product["file_path"],
        title=product["title"],
        description=product["description"],
        price=product["price"],
    )

    return {
        "status": "success",
        "product": product["title"],
        "download_path": product["file_path"],
        "engine_result": result,
    }

