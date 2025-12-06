# -----------------------------------------------------------
# JRAVIS WORKER — Batch 10 Auto Marketplace Uploader
# -----------------------------------------------------------

import os
import time
import json
import requests

BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")

def upload_template(name):
    print(f"[Uploader] Uploading {name} ...")
    try:
        res = requests.post(f"{BACKEND}/api/uploader/upload",
                            json={"name": name}).json()
        print("[Uploader] Upload result:", json.dumps(res, indent=2))
    except Exception as e:
        print("[Uploader] ERROR:", e)

def process():
    """
    Automatically checks for freshly generated templates
    and uploads them to all marketplaces.
    """
    print("[Uploader] Checking for new templates...")

    try:
        res = requests.get(f"{BACKEND}/api/factory/list").json()
        templates = res.get("templates", [])
    except:
        print("[Uploader] Cannot fetch template list.")
        return

    for t in templates:
        if not t.get("uploaded", False):
            upload_template(t["name"])

            # Mark template as uploaded
            requests.post(f"{BACKEND}/api/factory/mark_uploaded",
                          json={"name": t["name"]})

def main():
    print("🚀 JRAVIS Batch-10 Uploader Worker Started")

    while True:
        process()
        print("⏳ Sleeping 15 minutes...\n")
        time.sleep(900)

if __name__ == "__main__":
    main()
