from fastapi import FastAPI, Depends

from unified_engine import run_all_streams_micro_engine
from services.api.publish import router as publish_router

app = FastAPI()


# -------------------------
# ROUTERS
# -------------------------
app.include_router(publish_router)


# -------------------------
# BASIC ROUTES
# -------------------------

@app.get("/")
def root():
    return {"status": "JRAVIS API running"}


@app.get("/healthz")
def health():
    return {"ok": True}


# -------------------------
# FACTORY ENGINE
# -------------------------

@app.post("/api/factory/generate")
def generate():
    try:
        result = run_all_streams_micro_engine()
        return {"status": "success", **result}
    except Exception as e:
        return {"status": "error", "msg": str(e)}
