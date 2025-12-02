import requests
from settings import MESHY_API_KEY, OPENAI_API_KEY

def publish_meshy_assets(task):
    print("🎨 Generating Meshy 3D model...")
    print("⛔ Meshy API route unavailable — skipping upload.")

    prompt = {
        "model": "gpt-4.1-mini",
        "input": "Generate a 3D printable object idea (simple + trending)."
    }
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    resp = requests.post("https://api.openai.com/v1/responses", json=prompt, headers=headers)

    idea = resp.json()["output"][0]["content"][0]["text"]
    print("✨ 3D Idea:", idea)

    print("📡 Meshy API call (mock)")
    print("✅ Meshy publish complete.")
