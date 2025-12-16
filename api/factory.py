# ===============================
# FACTORY API – JRAVIS BACKEND
# ===============================

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
import uuid
import zipfile

router = APIRouter()

# -------------------------------
# PATHS
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FACTORY_OUTPUT_DIR = os.path.join(BASE_DIR, "..", "factory_output")
os.makedirs(FACTORY_OUTPUT_DIR, exist_ok=True)

# -------------------------------
# FACTORY GENERATE (EXAMPLE)
# -------------------------------
@router.post("/api/factory/generate")
def generate_factory_zip():
    """
    Generates a ZIP on backend filesystem
    """
    name = f"template-{uuid.uuid4().hex[:4]}"
    zip_path = os.path.join(FACTORY_OUTPUT_DIR, f"{name}.zip")

    # Dummy ZIP generation (replace with real logic)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr("README.txt", "JRAVIS TEMPLATE PACKAGE")

    return {
        "status": "generated",
        "name": name,
        "zip": f"factory_output/{name}.zip"
    }

# -------------------------------
# FACTORY ZIP DOWNLOAD (CRITICAL)
# -------------------------------
@router.get("/api/factory/download/{name}")
def download_factory_zip(name: str):
    """
    Allows worker to download ZIP via HTTP
    """
    zip_path = os.path.join(FACTORY_OUTPUT_DIR, f"{name}.zip")

    if not os.path.exists(zip_path):
        raise HTTPException(status_code=404, detail="ZIP not found")

    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename=f"{name}.zip"
    )
