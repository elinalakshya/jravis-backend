# unified_engine.py (duplicate location to satisfy worker's path)
# Minimal, robust unified engine stub for JRAVIS worker import.

import logging
import traceback
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

try:
    from src.publishing_engine import run_publishers  # type: ignore
except Exception as _e:
    logger.warning("Optional module src.publishing_engine not available: %s", _e)
    def run_publishers(config: Optional[Dict[str, Any]] = None) -> None:  # type: ignore
        logger.info("stub run_publishers called (publishing_engine not installed)")
        return

try:
    from src.some_other_engine import run_other_handlers  # type: ignore
except Exception:
    def run_other_handlers(config: Optional[Dict[str, Any]] = None) -> None:  # type: ignore
        logger.info("stub run_other_handlers called (some_other_engine not installed)")
        return

def fetch_remote_config(url: str) -> Dict[str, Any]:
    logger.info("fetch_remote_config requested for url: %s", url)
    try:
        import json  # noqa: F401
        return {"source": url}
    except Exception:
        logger.exception("fetch_remote_config failed")
        return {}

def run_all_streams_micro_engine(config: Optional[Dict[str, Any]] = None) -> None:
    logger.info("run_all_streams_micro_engine starting")
    if config is None:
        config = {}

    try:
        run_publishers(config)
    except Exception:
        logger.exception("run_publishers failed in unified engine")

    try:
        run_other_handlers(config)
    except Exception:
        logger.exception("run_other_handlers failed in unified engine")

    logger.info("run_all_streams_micro_engine finished")

if __name__ == "__main__":  # pragma: no cover
    logging.basicConfig(level=logging.INFO)
    try:
        run_all_streams_micro_engine({"local_test": True})
    except Exception:
        logger.error("unified_engine main runner failed:\n%s", traceback.format_exc())
