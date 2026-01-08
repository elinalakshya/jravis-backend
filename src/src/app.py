from fastapi import FastAPI, Query
import os

from draft_engine import (
    generate_and_save_template_draft,
    generate_batch_templates
)

app = FastAPI(title="JRAVIS Backend", version="1.0")


# -----------------------
# Health Endpoints
# -----------------------

@app.get("/")
def health():
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


# -----------------------
# Draft Generation APIs
# -----------------------

# Single draft generation
@app.post("/api/drafts/templates/generate")
def generate_template():
    draft, path = generate_and_save_template_draft()
    return {
        "status": "success",
        "path": path,
        "draft": draft
    }


# Batch draft generation
@app.post("/api/drafts/templates/batch")
def generate_batch(count: int = Query(10, ge=1, le=100)):
    results = generate_batch_templates(count)
    return {
        "status": "success",
        "generated": len(results),
        "items": results
    }


# -----------------------
# Legacy Endpoint (Disabled Safely)
# -----------------------

@app.post("/api/factory/generate")
def legacy_factory_disabled():
    return {
        "status": "disabled",
        "message": "Legacy factory endpoint disabled. Use /api/drafts/templates/*"
    }

