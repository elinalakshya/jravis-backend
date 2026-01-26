from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from unified_engine import run_draft_engine
from draft_store import load_drafts
import os

from fastapi import FastAPI
from services.api.publish import router as publish_router
app = FastAPI()
app.include_router(publish_router)
@app.get("/healthz")
def health():
    return {"status": "ok"}


@app.get("/")
def home():
    return {"status": "JRAVIS API running"}


@app.post("/api/draft/generate")
def generate_draft(niche: str = Query("general")):
    entry = run_draft_engine(niche)
    return {
        "status": "success",
        "product": entry["title"],
        "niche": niche,
        "download_zip": entry["zip"]
    }


@app.get("/api/drafts")
def list_drafts():
    return load_drafts()


@app.get("/download/{path:path}")
def download(path: str):
    if not os.path.exists(path):
        return {"error": "file not found"}
    return FileResponse(path, filename=os.path.basename(path))
