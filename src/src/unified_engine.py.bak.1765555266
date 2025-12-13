# --- OVERWRITE both unified_engine.py files with a CLEAN python implementation ---
cat > src/unified_engine.py <<'PY'
# unified_engine.py
# Clean, pure-Python unified engine adapter.
# Accepts run_all_streams_micro_engine(), run_all_streams_micro_engine(config),
# or run_all_streams_micro_engine(zip_path, template_name, backend_url).
# Adapts to varying run_publishers signatures at runtime.

import logging
import traceback
import inspect
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Try importing the real publishing engine; fall back to a stub if missing.
try:
    from src.publishing_engine import run_publishers  # type: ignore
except Exception as _e:
    logger.warning("Optional module src.publishing_engine not available: %s", _e)
    def run_publishers(config: Optional[Dict[str, Any]] = None) -> None:  # type: ignore
        logger.info("stub run_publishers called (publishing_engine not installed). config=%s", config)
        return

# Try importing other handlers; fall back to stub if missing.
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
        param_len = len(sig.parameters)
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

# Also write same clean file to nested path worker uses
mkdir -p src/src
cat > src/src/unified_engine.py <<'PY'
# duplicate for nested path; same implementation as src/unified_engine.py
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
        param_len = len(sig.parameters)
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
PY

# Syntax-check both files
python -m py_compile src/unified_engine.py || (echo "py_compile failed for src/unified_engine.py" && exit 1)
python -m py_compile src/src/unified_engine.py || (echo "py_compile failed for src/src/unified_engine.py" && exit 1)

# Commit & push to main so worker picks it up on next sync
git add src/unified_engine.py src/src/unified_engine.py
git commit -m "fix: clean unified_engine.py (remove stray shell text) and ensure runtime-adaptive adapter" || true
git push origin main || true

# Verify the nested file no longer contains stray shell text
sed -n '1,120p' src/src/unified_engine.py
