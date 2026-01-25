import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from unified_engine import run_all_streams_micro_engine

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "factory_output"))


@app.get("/")
def root():
    return {"status": "JRAVIS DRAFT FACTORY ONLINE"}


@app.get("/healthz")
def health():
    return {"ok": True}


@app.post("/api/factory/generate")
def generate_factory_product():
    try:
        product = run_all_streams_micro_engine()

        filename = product["zip_path"]
        download_url = f"/api/factory/download/{filename}"

        return {
            "status": "success",
            "product": product["title"],
            "price": product["price"],
            "download": download_url,
        }

    except Exception as e:
        return {"status": "error", "msg": str(e)}


@app.get("/api/factory/download/{filename}")
def download_file(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        file_path,
        filename=filename,
        media_type="application/zip",
    )
