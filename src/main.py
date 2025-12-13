from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os
import uuid
import zipfile

app = FastAPI()

# 🔥 CRITICAL FIX: anchor paths to this file location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FACTORY_DIR = os.path.join(BASE_DIR, "factory_output")

os.makedirs(FACTORY_DIR, exist_ok=True)

# --------------------------------------------------
# HEALTH
# --------------------------------------------------
@app.get("/healthz")
def health():
    return {"status": "ok"}

# --------------------------------------------------
# FACTORY: GENERATE ZIP
# --------------------------------------------------
@app.post("/api/factory/generate")
def generate_template():
    name = f"template-{uuid.uuid4().hex[:4]}"
    zip_name = f"{name}.zip"
    zip_path = os.path.join(FACTORY_DIR, zip_name)

    with zipfile.ZipFile(zip_path, "w") as z:
        z.writestr("README.txt", f"Generated template {name}")

    return {
        "status": "generated",
        "name": name,
        "zip": f"factory_output/{zip_name}",
    }

# --------------------------------------------------
# FACTORY: DOWNLOAD ZIP (🔥 NOW WORKS)
# --------------------------------------------------
@app.get("/api/factory/download/{filename}")
def download_factory_zip(filename: str):
    file_path = os.path.join(FACTORY_DIR, filename)

    if not os.path.isfile(file_path):
        raise HTTPException(
            status_code=404,
            detail=f"ZIP not found: {file_path}",
        )

    return FileResponse(
        path=file_path,
        media_type="application/zip",
        filename=filename,
    )

# --------------------------------------------------
# FACTORY: SCALE
# --------------------------------------------------
@app.post("/api/factory/scale/{name}")
def scale_factory(name: str):
    return {"status": "scaled", "name": name}

# --------------------------------------------------
# GROWTH
# --------------------------------------------------
@app.post("/api/growth/evaluate")
def growth_evaluate():
    return {
        "template": "unknown",
        "score": 50,
        "winner": False,
        "action": "pause",
    }
