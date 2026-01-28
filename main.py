from fastapi import FastAPI

from api.factory import router as factory_router
from jravis_backend.services.api.publish import router as publish_router

app = FastAPI(title="JRAVIS Backend")

app.include_router(factory_router)
app.include_router(publish_router)

@app.get("/healthz")
def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"status": "JRAVIS API running"}
