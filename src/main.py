from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os
import uuid
import zipfile

app = FastAPI()

BASE_DIR = os.getcwd()
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

    # create dummy zip (replace with real generator later)
    with zipfile.ZipFile(zip_path, "w") as z:
        z.writestr("README.txt", f"Generated template {name}")

    return {
        "status": "generated",
        "name": name,
        "zip": f"factory_output/{zip_name}",
    }

# --------------------------------------------------
# FACTORY: DOWNLOAD ZIP (🔥 FIX)
# --------------------------------------------------
@app.get("/api/factory/download/{filename}")
def download_factory_zip(filename: str):
    file_path = os.path.join(FACTORY_DIR, filename)

    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="ZIP not found")

    return FileResponse(
        file_path,
        media_type="application/zip",
        filename=filename,
    )

# --------------------------------------------------
# FACTORY: SCALE (stub)
# --------------------------------------------------
@app.post("/api/factory/scale/{name}")
def scale_factory(name: str):
    return {"status": "scaled", "name": name}

# --------------------------------------------------
# GROWTH (stub)
# --------------------------------------------------
@app.post("/api/growth/evaluate")
def growth_evaluate():
    return {
        "template": "unknown",
        "score": 50,
        "winner": False,
        "action": "pause",
    }
