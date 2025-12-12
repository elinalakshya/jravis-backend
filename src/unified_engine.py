# unified_engine.py
# Minimal, robust unified engine stub for JRAVIS worker import.
# Place this file at src/unified_engine.py
# This file intentionally:
# - exposes run_all_streams_micro_engine so worker.py can import it
# - tries to import optional project modules but degrades gracefully if missing

import logging
import traceback
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


# Attempt to import project-specific engines; if they don't exist, create no-op fallbacks.
try:
    # Example: your project likely provides these; import if present.
    from src.publishing_engine import run_publishers  # type: ignore
except Exception as e:  # pragma: no cover
    logger.warning("Optional module src.publishing_engine not available: %s", e)

    def run_publishers(config: Optional[Dict[str, Any]] = None) -> None:  # type: ignore
        logger.info("stub run_publishers called (publishing_engine not installed)")
        return


try:
    from src.some_other_engine import run_other_handlers  # type: ignore
except Exception:
    # pick a safe fallback
    def run_other_handlers(config: Optional[Dict[str, Any]] = None) -> None:  # type: ignore
        logger.info("stub run_other_handlers called (some_other_engine not installed)")
        return


def fetch_remote_config(url: str) -> Dict[str, Any]:
    """
    Placeholder helper to fetch remote config. Keep minimal so it never fails import-time.
    Replace with real implementation when stable.
    """
    logger.info("fetch_remote_config requested for url: %s", url)
    try:
        # Lazy import to avoid hard dependency
        import json
        return {"source": url}
    except Exception:
        logger.exception("fetch_remote_config failed")
        return {}


def run_all_streams_micro_engine(config: Optional[Dict[str, Any]] = None) -> None:
    """
    Primary entrypoint expected by worker.py:
        from unified_engine import run_all_streams_micro_engine

    This function runs the main micro-engines. It will not raise ImportError if optional modules
    are missing — instead it logs and continues.
    """
    logger.info("run_all_streams_micro_engine starting")
    if config is None:
        config = {}

    # Example safe calls to project handlers
    try:
        run_publishers(config)
    except Exception:
        logger.exception("run_publishers failed in unified engine")

    try:
        run_other_handlers(config)
    except Exception:
        logger.exception("run_other_handlers failed in unified engine")

    logger.info("run_all_streams_micro_engine finished")


# Keep a small CLI test runner so you can run this file directly for smoke tests.
if __name__ == "__main__":  # pragma: no cover
    logging.basicConfig(level=logging.INFO)
    try:
        run_all_streams_micro_engine({"local_test": True})
    except Exception:
        logger.error("unified_engine main runner failed:\n%s", traceback.format_exc())
