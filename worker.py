# File: worker.py
# JRAVIS Unified Worker - Advanced Production Version

import time
import traceback

# IMPORT ALL ENGINES
from src.engines.gumroad_engine import run_gumroad_engine
from src.engines.payhip_engine import run_payhip_engine
from src.engines.auto_blogging_engine import run_auto_blogging_engine
from src.engines.newsletter_content_engine import run_newsletter_content_engine
from src.engines.affiliate_funnel_engine import run_affiliate_funnel_engine
from src.engines.shopify_engine import run_shopify_engine
from src.engines.template_machine_engine import run_template_machine_engine

# IMPORT ALL PUBLISHERS
from publishers.gumroad_publisher import publish_gumroad
from publishers.payhip_publisher import publish_payhip
from publishers.blog_publisher import publish_blog
from publishers.newsletter_content_publisher import publish_newsletter
from publishers.affiliate_funnel_publisher import publish_affiliate_funnel
from publishers.shopify_publisher import publish_shopify
from publishers.template_machine_publisher import publish_template_machine


def log(msg: str):
    """Simple logger function (Render-friendly)."""
    print(f"[JRAVIS] {msg}", flush=True)


def safe_run(name: str, func, *args, **kwargs):
    """
    Runs any function safely.
    If it crashes, we return a JSON error payload.
    """
    try:
        log(f"Running {name}...")
        result = func(*args, **kwargs)
        log(f"{name} completed.")
        return {"success": True, "payload": result}
    except Exception as e:
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e),
            "trace": traceback.format_exc(),
        }


def run_all_streams():
    """
    MASTER RUNNER
    Runs each engine → sends to matching publisher → logs output.
    """

    log("JRAVIS Worker Started.")
    start_time = time.time()

    all_results = {}

    # ENGINE → PUBLISHER PIPELINES
    pipelines = [
        ("gumroad", run_gumroad_engine, publish_gumroad),
        ("payhip", run_payhip_engine, publish_payhip),
        ("auto_blogging", run_auto_blogging_engine, publish_blog),
        ("newsletter", run_newsletter_content_engine, publish_newsletter),
        ("affiliate_funnel", run_affiliate_funnel_engine, publish_affiliate_funnel),
        ("shopify", run_shopify_engine, publish_shopify),
        ("template_machine", run_template_machine_engine, publish_template_machine),
    ]
    
def write_log(text):
    with open("/opt/render/project/src/worker.log", "a") as f:
        f.write(text + "\n")

    # EXECUTE PIPELINES
    for stream_name, engine_fn, publisher_fn in pipelines:
        log(f"=== {stream_name.upper()} STREAM START ===")

        # Run engine safely
        engine_output = safe_run(f"{stream_name} engine", engine_fn)
        if not engine_output["success"]:
            all_results[stream_name] = {
                "success": False,
                "step": "engine",
                "error": engine_output["error"],
            }
            continue

        payload = engine_output["payload"]["data"]

        # Run publisher safely
        publish_output = safe_run(f"{stream_name} publisher", publisher_fn, payload)
        all_results[stream_name] = publish_output

        log(f"=== {stream_name.upper()} STREAM END ===\n")

    total_time = round(time.time() - start_time, 2)
    log(f"JRAVIS Worker Finished. Total time: {total_time}s")

    return all_results


if __name__ == "__main__":
    log("JRAVIS Worker Booting...")
    results = run_all_streams()
    log("Final Output:")
    print(results)
