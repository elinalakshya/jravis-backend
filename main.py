# ===============================
# JRAVIS BACKEND – MAIN
# ===============================

from fastapi import FastAPI
from api.factory import router as factory_router

app = FastAPI(title="JRAVIS Backend")

# -------------------------------
# ROUTERS
# -------------------------------
app.include_router(factory_router)

# -------------------------------
# HEALTH CHECK
# -------------------------------
@app.get("/healthz")
def health_check():
    return {"status": "ok"}
