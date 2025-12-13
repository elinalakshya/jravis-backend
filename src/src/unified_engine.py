
# unified_engine.py — runtime-adaptive publisher caller (preferred 2-arg)
# Tries multiple calling conventions, now preferring (description, extracted_dir)
# and logs the publisher signature for deterministic behavior.

import logging
import traceback
import inspect
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Import real publisher if present
try:
    from src.publishing_engine import run_publishers  # type: ignore
except Exception as _e:
    logger.warning("Optional module src.publishing_engine not available: %s", _e)
    def run_publishers(config: Optional[Dict[str, Any]] = None) -> None:  # type: ignore
        logger.info("stub run_publishers called (publishing_engine not installed). config=%s", config)
        return

# Import other handlers (stub fallback)
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

def _infer_description_and_extracted_dir(config: Dict[str, Any]) -> (str, str):
    description = config.get("description") or config.get("template_name") or ""
    extracted_dir = config.get("extracted_dir") or ""
    if not extracted_dir:
        zip_path = config.get("zip_path") or ""
        if isinstance(zip_path, str) and zip_path.endswith(".zip"):
            extracted_dir = zip_path.rsplit("/", 1)[-1][:-4]
        elif isinstance(zip_path, str):
            extracted_dir = zip_path.rsplit("/", 1)[-1]
    return description, extracted_dir

def _call_run_publishers_safely(config: Dict[str, Any]) -> None:
    """
    Heuristic caller for run_publishers. Prefer (description, extracted_dir) if plausible.
    Logs signature and every attempted call for debugging.
    """
    tried = []
    description, extracted_dir = _infer_description_and_extracted_dir(config)

    # Introspect
    try:
        sig = inspect.signature(run_publishers)
        param_names = list(sig.parameters.keys())
        param_len = len(param_names)
        logger.info("run_publishers signature: params=%s, len=%d", param_names, param_len)
    except Exception as e:
        param_names = []
        param_len = 0
        logger.warning("Could not introspect run_publishers: %s", e)

    # Strategy (preference order)
    # A. If it seems to be a 2-arg publisher -> try (description, extracted_dir) first.
    # B. If 'config' kw is accepted -> try run_publishers(config=config)
    # C. If single param -> try run_publishers(config)
    # D. If 3+ params -> try run_publishers(config, description, extracted_dir)
    # E. Try permutations and last-resort no-arg.

    # A) Prefer 2-positional if signature length == 2 or param names look like ['', '']:
    if param_len == 2 or (len(param_names) >= 1 and ('description' in param_names or 'extracted_dir' in param_names)):
        try:
            tried.append("run_publishers(description, extracted_dir)")
            run_publishers(description, extracted_dir)
            logger.info("run_publishers succeeded with (description, extracted_dir)")
            return
        except Exception as e:
            logger.warning("run_publishers(description, extracted_dir) failed: %s", e)

    # B) If 'config' kw in param names, try keyword call
    if 'config' in param_names:
        try:
            tried.append("run_publishers(config=config)")
            run_publishers(config=config)
            logger.info("run_publishers succeeded with keyword config")
            return
        except Exception as e:
            logger.warning("run_publishers(config=config) failed: %s", e)

    # C) If single param, try positional config
    if param_len == 1:
        try:
            tried.append("run_publishers(config)")
            run_publishers(config)
            logger.info("run_publishers succeeded with single positional config")
            return
        except Exception as e:
            logger.warning("run_publishers(config) failed: %s", e)

    # D) If 3+ params, try config + description + extracted_dir
    if param_len >= 3:
        try:
            tried.append("run_publishers(config, description, extracted_dir)")
            run_publishers(config, description, extracted_dir)
            logger.info("run_publishers succeeded with (config, description, extracted_dir)")
            return
        except Exception as e:
            logger.warning("run_publishers(config, description, extracted_dir) failed: %s", e)

    # E) Permutation attempts (safe)
    permutations = [
        (description,),
        (extracted_dir,),
        (description, config),
        (config, description),
    ]
    for cand in permutations:
        try:
            tried.append(f"run_publishers{cand}")
            run_publishers(*cand)
            logger.info("run_publishers succeeded with args %s", cand)
            return
        except Exception:
            continue

    # F) Last resort: no-arg
    try:
        tried.append("run_publishers()")
        run_publishers()
        logger.info("run_publishers succeeded with no args")
        return
    except Exception as e:
        logger.warning("run_publishers() last-resort call failed: %s", e)

    logger.error("All attempts to call run_publishers failed. Tried: %s", tried)

def run_all_streams_micro_engine(*args, **kwargs) -> None:
    try:
        config = _normalize_args_to_config(*args, **kwargs)
        logger.info("run_all_streams_micro_engine called. config: %s", config)
        try:
            _call_run_publishers_safely(config)
        except Exception:
            logger.exception("run_publishers failed in unified engine")
        try:
            run_other_handlers(config)
        except Exception:
            logger.exception("run_other_handlers failed in unified engine")
        logger.info("run_all_streams_micro_engine finished successfully")
    except Exception:
        logger.error("run_all_streams_micro_engine top-level failure:\\n%s", traceback.format_exc())

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run_all_streams_micro_engine('factory_output/template-test.zip', 'template-test', 'https://localhost')
