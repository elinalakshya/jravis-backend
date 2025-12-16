from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import io
import zipfile
import uuid

app = FastAPI()

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/api/factory/generate")
def factory_generate():
    name = f"template-{uuid.uuid4().hex[:4]}"

    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("README.txt", "JRAVIS STREAM PACKAGE")

    buffer.seek(0)

    # IMPORTANT: filename is the source of truth
    return StreamingResponse(
        buffer,
        media_type="application/zip",
        headers={
            "Content-Disposition": f'attachment; filename="{name}.zip"'
        }
    )
