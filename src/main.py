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
def generate_template():
    """
    Streams a ZIP file directly to the worker.
    NO local filesystem dependency.
    SAFE on Render.
    """
    template_name = f"template-{uuid.uuid4().hex[:4]}"

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(
            "README.txt",
            f"JRAVIS generated template: {template_name}"
        )

    zip_buffer.seek(0)

    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={
            "Content-Disposition": f'attachment; filename="{template_name}.zip"',
            "X-Template-Name": template_name
        }
    )
