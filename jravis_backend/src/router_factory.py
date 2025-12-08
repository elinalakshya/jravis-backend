from fastapi import APIRouter
import uuid, os, zipfile

router = APIRouter()

@router.post("/generate")
def generate_template():
    name = f"template-{uuid.uuid4().hex[:4]}"
    zip_path = f"factory_output/{name}.zip"

    os.makedirs("factory_output", exist_ok=True)

    # Create a REAL zip file
    with zipfile.ZipFile(zip_path, "w") as z:
        z.writestr("README.txt", f"This is the content for {name}")

    return {"status": "generated", "name": name, "zip": zip_path}

@router.post("/scale/{name}")
def scale(name: str):
    return {"status": "scaled", "name": name}
