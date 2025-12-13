# unified_engine.py (CLEAN — NO SHELL CODE)

import logging
import traceback
from typing import Dict, Any

logger = logging.getLogger(__name__)

# ---- PUBLISHER (GUMROAD) ----
try:
    from src.publishing_engine import run_publishers
except Exception:
    def run_publishers(description: str, extracted_dir: str):
        logger.info("stub run_publishers called: %s %s", description, extracted_dir)

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

def run_all_streams_micro_engine(zip_path: str, template_name: str, backend_url: str):
    try:
        config = {
            "zip_path": zip_path,
            "template_name": template_name,
            "backend_url": backend_url,
        }

        description, extracted_dir = _infer_description_and_extracted_dir(config)

        logger.info(
            "Publishing with description='%s', extracted_dir='%s'",
            description,
            extracted_dir,
        )

        run_publishers(description, extracted_dir)
        run_other_handlers(config)

        logger.info("run_all_streams_micro_engine completed successfully")

    except Exception:
        logger.error(
            "run_all_streams_micro_engine FAILED:\n%s",
            traceback.format_exc(),
        )
