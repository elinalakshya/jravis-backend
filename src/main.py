from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os
import uuid
import zipfile

app = FastAPI()

# =====================================================
# ABSOLUTE, VERIFIED FACTORY DIRECTORY (RENDER SAFE)
# =====================================================
FACTORY_OUTPUT_DIR = "/opt/render/project/src/factory_output"
os.makedirs(FACTORY_OUTPUT_DIR, exist_ok=True)

print("📁 BACKEND FACTORY_OUTPUT_DIR =", FACTORY_OUTPUT_DIR)
print("📂 DIR CONTENTS AT START =", os.listdir(FACTORY_OUTPUT_DIR))

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

    print("🧪 ATTEMPTING ZIP CREATE:", zip_path)

    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("README.txt", "JRAVIS PACKAGE")
    except Exception as e:
        print("❌ ZIP WRITE FAILED:", e)
        raise HTTPException(status_code=500, detail="ZIP write failed")

    # HARD VERIFY
    if not os.path.exists(zip_path):
        print("❌ ZIP NOT FOUND AFTER WRITE")
        print("📂 DIR CONTENTS =", os.listdir(FACTORY_OUTPUT_DIR))
        raise HTTPException(status_code=500, detail="ZIP missing after creation")

    print("✅ ZIP CREATED:", zip_path)
    print("📂 DIR CONTENTS =", os.listdir(FACTORY_OUTPUT_DIR))

    return {
        "status": "generated",
        "name": name
    }

# -----------------------
# FACTORY DOWNLOAD
# -----------------------
@app.get("/api/factory/download/{name}")
def factory_download(name: str):
    zip_path = os.path.join(FACTORY_OUTPUT_DIR, f"{name}.zip")

    print("📦 DOWNLOAD CHECK:", zip_path)
    print("📂 DIR CONTENTS =", os.listdir(FACTORY_OUTPUT_DIR))

    if not os.path.exists(zip_path):
        raise HTTPException(status_code=404, detail="ZIP not found")

    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename=f"{name}.zip"
    )
