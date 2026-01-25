from fastapi import FastAPI
from unified_engine import run_all_streams_micro_engine

app = FastAPI()


@app.get("/")
def root():
    return {"status": "JRAVIS API running"}


@app.get("/healthz")
def health():
    return {"ok": True}


@app.post("/api/factory/generate")
def generate():
    try:
        result = run_all_streams_micro_engine()
        return {"status": "success", **result}
    except Exception as e:
        return {"status": "error", "msg": str(e)}
