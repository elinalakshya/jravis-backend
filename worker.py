# -----------------------------------------------------------
# JRAVIS WORKER — Batch 9 (Balanced Factory Mode)
# Auto-Scaling Templates + Funnels + Marketplace Publishing
# -----------------------------------------------------------

import os
import time
import random
import requests

BACKEND = os.getenv("JRAVIS_BACKEND", "https://jravis-backend.onrender.com")
N8N_WEBHOOK = os.getenv("N8N_WEBHOOK_URL")  # Ensure this is set in Render

LOCK = os.getenv("JRAVIS_LOCK", "JRV2040_LOCKED_KEY_001")

# -----------------------------------------------------------
# Balanced Factory Output (15–30 assets weekly)
# -----------------------------------------------------------

def generate_factory_batch():
    count = random.randint(15, 30)

    categories = [
        "webflow_template",
        "gumroad_template",
        "payhip_template",
        "ai_funnel",
        "etsy_digital_product",
        "shopify_digital_product",
        "pod_listing",
        "ai_landing_page",
    ]

    tasks = []
    for _ in range(count):
        c = random.choice(categories)
        tasks.append({
            "type": "factory_asset",
            "category": c,
            "title": f"JRAVIS Auto {' '.join(c.split('_')).title()} #{random.randint(1000,9999)}",
        })

    return tasks


# -----------------------------------------------------------
# Send Task to Backend Queue
# -----------------------------------------------------------

def queue_task(task):
    try:
        res = requests.post(
            f"{BACKEND}/task/new",
            json={"task": task, "lock": LOCK},
            timeout=10
        )
        return res.json()
    except Exception as e:
        return {"error": str(e)}


# -----------------------------------------------------------
# Push Summary to n8n (optional)
# -----------------------------------------------------------

def push_to_n8n(summary):
    if not N8N_WEBHOOK:
        return {"status": "no_n8n_webhook_defined"}

    try:
        res = requests.post(N8N_WEBHOOK, json=summary, timeout=10)
        return {"sent_to_n8n": res.status_code}
    except Exception as e:
        return {"n8n_error": str(e)}


# -----------------------------------------------------------
# MAIN LOOP — Runs weekly (Balanced Factory Mode)
# -----------------------------------------------------------

def main():
    print("🔥 JRAVIS Worker — Batch 9 Factory Mode Enabled (Balanced)")

    while True:
        print("\n🚀 Starting Weekly Factory Cycle…")

        batch = generate_factory_batch()

        results = []
        for item in batch:
            r = queue_task(item)
            results.append(r)

        summary = {
            "mode": "balanced",
            "assets_created": len(batch),
            "details": results[:5],  # send only 5 items to n8n for shorter payload
        }

        print("📦 Factory Batch Summary:", summary)

        # push weekly summary to N8N
        push_to_n8n(summary)

        print("⏳ Sleeping 7 days… (Balanced Weekly Mode)\n")
        time.sleep(7 * 24 * 3600)


if __name__ == "__main__":
    main()
