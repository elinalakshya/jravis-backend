from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import io
import zipfile
import uuid

print("🚨 BACKEND VERSION = STREAM-ONLY-ACTIVE")

app = FastAPI()

# -----------------------
# HEALTH CHECK
# -----------------------
@app.get("/healthz")
def healthz():
    return {"status": "ok"}

# -----------------------
# FACTORY GENERATE (STREAM ZIP ONLY)
# -----------------------
@app.post("/api/factory/generate")
def factory_generate():
    """
    STREAM-ONLY endpoint.
    Returns ZIP bytes, NEVER JSON.
    """

    name = f"template-{uuid.uuid4().hex[:4]}"

    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("README.txt", "JRAVIS STREAM PACKAGE")

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/zip"
    )
