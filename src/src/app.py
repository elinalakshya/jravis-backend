<<<<<<< HEAD
# src/src/app.py
=======
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os
>>>>>>> 1f57279cb1e2a7d049ea5ef7a4b8c6cf7fd106fa

from fastapi import FastAPI
from product_factory import generate_product
from unified_engine import run_all_streams_micro_engine

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "..", "factory_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.get("/")
def root():
    return {"status": "JRAVIS API running"}


@app.get("/healthz")
def health():
    return {"ok": True}


<<<<<<< HEAD
=======
# -----------------------------
# FACTORY GENERATE
# -----------------------------
>>>>>>> 1f57279cb1e2a7d049ea5ef7a4b8c6cf7fd106fa
@app.post("/api/factory/generate")
def factory_generate():
    print("🔥 FACTORY API TRIGGERED")

    product = generate_product()
<<<<<<< HEAD

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

=======

    file_path = product["file_path"]
    title = product["title"]
    description = product["description"]
    price = product["price"]

    print("📦 PRODUCT TITLE:", title)
    print("📄 PRODUCT FILE :", file_path)
    print("💰 PRICE        :", price)

    try:
        run_all_streams_micro_engine(
            file_path=file_path,
            title=title,
            description=description,
            price=price,
        )
    except Exception as e:
        return {"status": "error", "msg": str(e)}

    filename = os.path.basename(file_path)

    return {
        "status": "success",
        "product": title,
        "download_url": f"/api/factory/download/{filename}",
    }


# -----------------------------
# DOWNLOAD
# -----------------------------
@app.get("/api/factory/download/{filename}")
def download_file(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream",
    )
>>>>>>> 1f57279cb1e2a7d049ea5ef7a4b8c6cf7fd106fa
