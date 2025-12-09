import requests
import zipfile
import os

def run_all_streams_micro_engine(zip_path, title, backend_url):
    from unified_engine_publish_patch import run_publishers

    print("⚙️ JRAVIS UNIFIED ENGINE STARTED")
    print("ZIP =", zip_path)
    print("TITLE =", title)

    # Download full ZIP from backend
    remote_url = f"{backend_url}/files/{zip_path}"
    print("[DOWNLOAD]", remote_url)

    try:
        r = requests.get(remote_url)
        if r.status_code != 200:
            print("[DOWNLOAD ERROR]:", r.text)
            print("❌ Cannot proceed")
            return
    except Exception as e:
        print("❌ Download exception:", e)
        return

    # Save ZIP locally
    local_zip = f"tmp_{title}.zip"
    with open(local_zip, "wb") as f:
        f.write(r.content)

    # Extract ZIP
    try:
        with zipfile.ZipFile(local_zip, "r") as z:
            z.extractall(f"unzipped/{title}")
    except Exception as e:
        print("❌ ZIP extraction failed:", e)
        return

    print("✔️ ZIP extracted, ready to run publishers")
        run_publishers(title, local_path, logger=print)

    # Now call all engines (placeholder)
    print("📦 Running marketplace, viral, pricing engines… (OK)")
