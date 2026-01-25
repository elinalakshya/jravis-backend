from fastapi import FastAPI

from product_factory import generate_product
from unified_engine import run_all_streams_micro_engine

app = FastAPI()


# -----------------------------
# HEALTH
# -----------------------------

@app.get("/")
def root():
    return {"status": "JRAVIS running"}

@app.get("/healthz")
def health():
    return {"status": "ok"}


# -----------------------------
# FACTORY → PUBLISH PIPELINE
# -----------------------------
from unified_engine import run_all_streams_micro_engine

@app.post("/api/factory/generate")
def factory_generate():

    product = generate_product()

    try:
        result = run_all_streams_micro_engine(
            file_path=product["file_path"],
            title=product["title"],
            price=product["price"]
        )

        return {
            "status": "success",
            "product": product["title"],
            "publish_result": result
        }

    except Exception as e:
        return {
            "status": "error",
            "msg": str(e),
            "product": product
        }


    except Exception as e:
        print("❌ FACTORY ERROR:", e)
        return {"status": "error", "msg": str(e)}

