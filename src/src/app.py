from fastapi import FastAPI
import os
import json
from pathlib import Path

from draft_engine import (
    generate_and_save_template_draft,
    generate_batch_templates
)

# -----------------------------
# App Setup
# -----------------------------
app = FastAPI(title="JRAVIS Backend", version="1.0")

DATA_DIR = Path("/opt/render/project/src/data/drafts/templates")

# -----------------------------
# Health Endpoints
# -----------------------------
@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "jravis",
        "env": os.getenv("ENV", "prod")
    }


@app.get("/ping")
def ping():
    return {"message": "JRAVIS is alive 🚀"}


@app.get("/healthz")
def healthz():
    return {"status": "healthy"}


# -----------------------------
# Draft APIs
# -----------------------------

@app.post("/api/drafts/templates/generate")
def generate_template():
    draft, path = generate_and_save_template_draft()
    return {
        "status": "success",
        "path": path,
        "draft": draft
    }


@app.post("/api/drafts/templates/batch")
def generate_batch(count: int = 10):
    items = generate_batch_templates(count)
    return {
        "status": "success",
        "generated": len(items),
        "items": items
    }


@app.get("/api/drafts/templates")
def list_templates():
    items = []

    if DATA_DIR.exists():
        for f in DATA_DIR.glob("*.json"):
            try:
                data = json.loads(f.read_text())
                items.append({
                    "id": data.get("id"),
                    "title": data.get("title"),
                    "path": str(f)
                })
            except Exception:
                pass

    return {
        "count": len(items),
        "items": items[-50:]
    }


@app.get("/api/drafts/templates/{draft_id}")
def get_template(draft_id: str):
    file = DATA_DIR / f"{draft_id}.json"

    if not file.exists():
        return {"error": "Draft not found"}

    return json.loads(file.read_text())

