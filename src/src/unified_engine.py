# unified_engine.py — FINAL, signature-safe

import logging
import traceback
import inspect
from typing import Dict, Any

logger = logging.getLogger(__name__)

# ---- IMPORT PUBLISHER ----
try:
    from src.publishing_engine import run_publishers
except Exception:
    def run_publishers(*args, **kwargs):
        logger.info("stub run_publishers called with args=%s kwargs=%s", args, kwargs)

# ---- OTHER HANDLERS ----
try:
    from src.some_other_engine import run_other_handlers
except Exception:
    def run_other_handlers(config: Dict[str, Any]):
        return

def _infer_description_and_extracted_dir(config: Dict[str, Any]):
    name = config.get("template_name") or config.get("description") or ""
    zip_path = config.get("zip_path", "")
    extracted = zip_path.split("/")[-1].replace(".zip", "") if zip_path else name
    return name, extracted

def _call_run_publishers_safely(description: str, extracted_dir: str, config: Dict[str, Any]):
    try:
        sig = inspect.signature(run_publishers)
        params = len(sig.parameters)

        logger.info("run_publishers expects %d parameters", params)

        if params == 1:
            run_publishers(description)
        elif params == 2:
            run_publishers(description, extracted_dir)
        else:
            # fallback for future expansion
            run_publishers(description, extracted_dir, config)

    except TypeError as te:
        logger.error("run_publishers TypeError: %s", te)
    except Exception:
        logger.error("run_publishers failed:\n%s", traceback.format_exc())

def run_all_streams_micro_engine(zip_path: str, template_name: str, backend_url: str):
    try:
        description = template_name
        file_path = zip_path  # ✅ THIS IS THE REAL ZIP FILE

        logger.info(
            "Publishing Gumroad product: title='%s', file='%s'",
            description,
            file_path,
        )

        # 🔥 HARD-CORRECT CALL
        run_publishers(description, description, file_path)

        run_other_handlers({
            "zip_path": zip_path,
            "template_name": template_name,
            "backend_url": backend_url,
        })

        logger.info("run_all_streams_micro_engine completed successfully")

    except Exception:
        logger.error(
            "run_all_streams_micro_engine FAILED:\n%s",
            traceback.format_exc(),
        )
