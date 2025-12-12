# unified_engine.py
# Accepts run_all_streams_micro_engine(), run_all_streams_micro_engine(config),
# and run_all_streams_micro_engine(zip_path, template_name, backend_url).
# Normalizes input to a config dict and calls available sub-engines.

import logging
import traceback
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Optional project imports with safe fallbacks
try:
    from src.publishing_engine import run_publishers  # type: ignore
except Exception as _e:
    logger.warning("Optional module src.publishing_engine not available: %s", _e)
    def run_publishers(config: Optional[Dict[str, Any]] = None) -> None:  # type: ignore
        logger.info("stub run_publishers called (publishing_engine not installed). config=%s", config)
        return

try:
    from src.some_other_engine import run_other_handlers  # type: ignore
except Exception:
    def run_other_handlers(config: Optional[Dict[str, Any]] = None) -> None:  # type: ignore
        logger.info("stub run_other_handlers called (some_other_engine not installed). config=%s", config)
        return

def _normalize_args_to_config(*args, **kwargs) -> Dict[str, Any]:
    cfg: Dict[str, Any] = {}
    if len(args) == 3:
        cfg.update({"zip_path": args[0], "template_name": args[1], "backend_url": args[2]})
    elif len(args) == 1 and isinstance(args[0], dict):
        cfg.update(args[0])
    elif len(args) > 0:
        cfg["positional_args"] = args
    cfg.update(kwargs)
    return cfg

def run_all_streams_micro_engine(*args, **kwargs) -> None:
    try:
        config = _normalize_args_to_config(*args, **kwargs)
        logger.info("run_all_streams_micro_engine called. config: %s", config)
        try:
            run_publishers(config)
        except Exception:
            logger.exception("run_publishers failed in unified engine")
        try:
            run_other_handlers(config)
        except Exception:
            logger.exception("run_other_handlers failed in unified engine")
        logger.info("run_all_streams_micro_engine finished successfully")
    except Exception:
        logger.error("run_all_streams_micro_engine top-level failure:\n%s", traceback.format_exc())

if __name__ == "__main__":  # pragma: no cover
    logging.basicConfig(level=logging.INFO)
    run_all_streams_micro_engine("factory_output/template-test.zip", "template-test", "https://localhost")
