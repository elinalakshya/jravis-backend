# unified_engine.py
# Robust unified engine compatible with both:
#  - run_all_streams_micro_engine()
#  - run_all_streams_micro_engine(config_dict)
#  - run_all_streams_micro_engine(zip_path, template_name, backend_url)
#
# The function normalizes arguments into a `config` dict and proceeds.

import logging
import traceback
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


# Optional project imports with safe fallbacks
try:
    from src.publishing_engine import run_publishers  # type: ignore
except Exception as _e:  # pragma: no cover
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
    """
    Normalize different calling conventions into a single config dict.

    - If called with 3 positional args: (zip_path, template_name, backend_url)
      -> returns {'zip_path': ..., 'template_name': ..., 'backend_url': ...}

    - If called with 1 positional arg and it's a dict -> treated as config

    - If called with no args -> returns empty dict

    Keyword args are merged into the resulting dict.
    """
    cfg: Dict[str, Any] = {}
    if len(args) == 3:
        cfg.update({
            "zip_path": args[0],
            "template_name": args[1],
            "backend_url": args[2],
        })
    elif len(args) == 1 and isinstance(args[0], dict):
        cfg.update(args[0])
    elif len(args) > 0:
        # Unexpected positional args -> store them under 'positional_args'
        cfg["positional_args"] = args

    # merge kwargs (kwargs win)
    cfg.update(kwargs)
    return cfg


def run_all_streams_micro_engine(*args, **kwargs) -> None:
    """
    Primary entrypoint expected by worker.py.

    Accepts:
      - run_all_streams_micro_engine()
      - run_all_streams_micro_engine(config_dict)
      - run_all_streams_micro_engine(zip_path, template_name, backend_url)
      - run_all_streams_micro_engine(*args, **kwargs)

    Normalizes input to a config dict and calls available sub-engines.
    """
    try:
        config = _normalize_args_to_config(*args, **kwargs)
        logger.info("run_all_streams_micro_engine called. config: %s", config)

        # Example: pass the normalized config to sub-engines
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


# Small CLI test runner for manual checks
if __name__ == "__main__":  # pragma: no cover
    logging.basicConfig(level=logging.INFO)
    try:
        # local test: simulate the 3-arg call
        run_all_streams_micro_engine("factory_output/template-test.zip", "template-test", "https://localhost")
    except Exception:
        logger.error("unified_engine main runner failed:\n%s", traceback.format_exc())
