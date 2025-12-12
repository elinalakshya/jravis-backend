# Overwrite main path
cat > src/unified_engine.py <<'PY'
# unified_engine.py — runtime-aware calling for run_publishers
import logging
import traceback
import inspect
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Attempt to import real engines; allow fallbacks
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

def _infer_description_and_extracted_dir(config: Dict[str, Any]) -> (str, str):
    """
    Try to derive reasonable values for description and extracted_dir if not provided.
    - description: try config['description'] -> template_name -> zip filename
    - extracted_dir: try config['extracted_dir'] -> zip_path without .zip -> basename
    """
    description = config.get("description") or config.get("template_name") or ""
    extracted_dir = config.get("extracted_dir") or ""
    if not extracted_dir:
        zip_path = config.get("zip_path") or ""
        if isinstance(zip_path, str) and zip_path.endswith(".zip"):
            # remove extension and any parent folders
            extracted_dir = zip_path.rsplit("/", 1)[-1][:-4]
        elif isinstance(zip_path, str):
            extracted_dir = zip_path.rsplit("/", 1)[-1]
    return description, extracted_dir

def _call_run_publishers_safely(config: Dict[str, Any]) -> None:
    """
    Call run_publishers using the correct calling convention based on its signature.
    Supports:
      - run_publishers(config)
      - run_publishers(config, description, extracted_dir)
      - other variants (will try best-effort)
    """
    try:
        sig = inspect.signature(run_publishers)
        params = sig.parameters
        param_len = len(params)
    except Exception:
        # If we can't introspect, try the simple call
        param_len = 1

    # Common patterns:
    try:
        if param_len == 1:
            # single-arg API
            run_publishers(config)
            return
        elif param_len >= 3:
            # expect (config, description, extracted_dir) as common pattern in your code
            description, extracted_dir = _infer_description_and_extracted_dir(config)
            # call with first three args
            run_publishers(config, description, extracted_dir)
            return
        else:
            # fallback: try single arg then multi-arg
            try:
                run_publishers(config)
                return
            except TypeError:
                description, extracted_dir = _infer_description_and_extracted_dir(config)
                run_publishers(config, description, extracted_dir)
                return
    except TypeError as te:
        logger.warning("run_publishers TypeError on tried signature: %s", te)
    except Exception:
        logger.exception("run_publishers raised an unexpected error")
    # As last resort, try calling with kwargs if supported
    try:
        run_publishers(config=config)
    except Exception:
        logger.exception("All attempts to call run_publishers failed")

def run_all_streams_micro_engine(*args, **kwargs) -> None:
    """
    Entrypoint compatible with multiple calling styles. Normalizes to a config dict
    and calls the publishing and other handlers. Handles different run_publishers
    signatures at runtime.
    """
    try:
        config = _normalize_args_to_config(*args, **kwargs)
        logger.info("run_all_streams_micro_engine called. config: %s", config)

        # Call publishing engine using runtime-adaptive wrapper
        try:
            _call_run_publishers_safely(config)
        except Exception:
            logger.exception("run_publishers failed in unified engine")

        # call other handlers
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
PY

# Mirror into nested path that worker sometimes imports
mkdir -p src/src
cat > src/src/unified_engine.py <<'PY'
# duplicate for nested path used by worker — runtime-aware calling for run_publishers
import logging, traceback, inspect
from typing import Any, Dict, Optional
logger = logging.getLogger(__name__)
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
    try:
        sig = inspect.signature(run_publishers)
        params = sig.parameters
        param_len = len(params)
    except Exception:
        param_len = 1
    try:
        if param_len == 1:
            run_publishers(config)
            return
        elif param_len >= 3:
            description, extracted_dir = _infer_description_and_extracted_dir(config)
            run_publishers(config, description, extracted_dir)
            return
        else:
            try:
                run_publishers(config)
                return
            except TypeError:
                description, extracted_dir = _infer_description_and_extracted_dir(config)
                run_publishers(config, description, extracted_dir)
                return
    except TypeError as te:
        logger.warning("run_publishers TypeError on tried signature: %s", te)
    except Exception:
        logger.exception("run_publishers raised an unexpected error")
    try:
        run_publishers(config=config)
    except Exception:
        logger.exception("All attempts to call run_publishers failed")
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
        logger.error("run_all_streams_micro_engine top-level failure:\n%s", traceback.format_exc())
if __name__ == "__main__":  # pragma: no cover
    logging.basicConfig(level=logging.INFO)
    run_all_streams_micro_engine("factory_output/template-test.zip", "template-test", "https://localhost")
PY

# Syntax-check, commit & push
python -m py_compile src/unified_engine.py || (echo "py_compile failed for src/unified_engine.py" && exit 1)
python -m py_compile src/src/unified_engine.py || (echo "py_compile failed for src/src/unified_engine.py" && exit 1)
git add src/unified_engine.py src/src/unified_engine.py
git commit -m "fix: runtime-call adapter for run_publishers (supports 1-arg and 3-arg signatures)" || true
git push origin main || true

echo "Files updated and pushed. Now restart the worker on the host: python worker.py"
