# ===============================
# JRAVIS BACKEND – MAIN APP
# ===============================

from fastapi import FastAPI

# Existing factory routes (already in your project)
from api.factory import router as factory_router

# POD publish routes (Printify -> Etsy drafts)
from jravis_backend.services.api.publish import router as publish_router


app = FastAPI(title="JRAVIS Backend")


# -------------------------------
# ROUTERS
# -------------------------------
app.include_router(factory_router)
app.include_router(publish_router)


# -------------------------------
# HEALTH CHECK
# -------------------------------
@app.get("/healthz")
def health_check():
    return {"status": "ok"}


# -------------------------------
# ROOT
# -------------------------------
@app.get("/")
def root():
    return {"status": "JRAVIS API running"}
