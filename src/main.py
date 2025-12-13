from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="JRAVIS Backend", version="1.0")

# -------------------------------------------------
# CORS (safe default)
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# HEALTH CHECK
# -------------------------------------------------
@app.get("/healthz")
def healthz():
    return {"status": "ok"}

# -------------------------------------------------
# FACTORY: GENERATE TEMPLATE
# (assumes your existing logic already creates ZIP)
# -------------------------------------------------
@app.post("/api/factory/generate")
def factory_generate():
    """
    Generates a template ZIP and stores it in factory_output/
    """
    import uuid

    name = f"template-{uuid.uuid4().hex[:4]}"
    os.makedirs("factory_output", exist_ok=True)

    zip_filename = f"{name}.zip"
    zip_path = os.path.join("factory_output", zip_filename)

    # ---- placeholder zip creation (replace with real logic) ----
    with open(zip_path, "wb") as f:
        f.write(b"PK\x05\x06")  # minimal empty zip marker
    # ------------------------------------------------------------

    return {
        "status": "generated",
        "name": name,
        "zip": zip_filename,  # IMPORTANT: filename only
    }

# -------------------------------------------------
# FACTORY: SCALE
# -------------------------------------------------
@app.post("/api/factory/scale/{name}")
def factory_scale(name: str):
    return {"status": "scaled", "name": name}

# -------------------------------------------------
# GROWTH: EVALUATE
# -------------------------------------------------
@app.post("/api/growth/evaluate")
def growth_evaluate():
    return {
        "template": "unknown",
        "score": 50,
        "winner": False,
        "action": "pause",
    }

# -------------------------------------------------
# ✅ FACTORY: DOWNLOAD ZIP (FIX)
# -------------------------------------------------
@app.get("/api/factory/download/{filename}")
def download_factory_zip(filename: str):
    """
    Secure download endpoint for worker.
    """
    base_dir = "factory_output"
    file_path = os.path.join(base_dir, filename)

    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="ZIP not found")

    return FileResponse(
        file_path,
        media_type="application/zip",
        filename=filename,
    )
