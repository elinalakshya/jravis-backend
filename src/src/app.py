from fastapi import FastAPI
import os

app = FastAPI(title="JRAVIS Backend", version="1.0")


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
    
