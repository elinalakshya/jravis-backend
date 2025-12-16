from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os
import uuid
import zipfile

app = FastAPI()

# -----------------------
# PATHS
# -----------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FACTORY_OUTPUT_DIR = os.path.join(BASE_DIR, "..", "factory_output")
os.makedirs(FACTORY_OUTPUT_DIR, exist_ok=True)

# -----------------------
# HEALTH CHECK
# -----------------------
@app.get("/healthz")
def healthz():
    return {"status": "ok"}

# -----------------------
# FACTORY GENERATE
# -----------------------
@app.post("/api/factory/generate")
def factory_generate():
    name = f"template-{uuid.uuid4().hex[:4]}"
    zip_path = os.path.join(FACTORY_OUTPUT_DIR, f"{name}.zip")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("README.txt", "JRAVIS PACKAGE")

    return {
        "status": "generated",
        "name": name,
        "zip": f"factory_output/{name}.zip"
    }

# -----------------------
# FACTORY DOWNLOAD (CRITICAL)
# -----------------------
@app.get("/api/factory/download/{name}")
def factory_download(name: str):
    zip_path = os.path.join(FACTORY_OUTPUT_DIR, f"{name}.zip")

    if not os.path.exists(zip_path):
        raise HTTPException(status_code=404, detail="ZIP not found")

    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename=f"{name}.zip"
    )
