from fastapi import FastAPI
import os

app = FastAPI(title="JRAVIS Backend", version="1.0")

from draft_engine import generate_and_save_template_draft

@app.post("/drafts/templates/generate")
def generate_template():
    draft, path = generate_and_save_template_draft()
    return {
        "status": "success",
        "path": path,
        "draft": draft
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
    
