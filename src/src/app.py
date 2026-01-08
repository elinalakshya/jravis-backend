from fastapi import FastAPI
import os

app = FastAPI(title="JRAVIS Backend", version="1.0")

from draft_engine import generate_and_save_template_draft

@app.post("/api/factory/generate")
def legacy_factory_disabled():
    return {
        "status": "disabled",
        "message": "Legacy factory endpoint disabled. Use /drafts/templates/generate"
    }

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
