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
        z.writestr("README.txt", "JRAVIS PACKAGE")
    buffer.seek(0)

    headers = {
        "X-Template-Name": name,
        "Content-Disposition": f'attachment; filename="{name}.zip"'
    }

    return StreamingResponse(
        buffer,
        media_type="application/zip",
        headers=headers
    )
