import requests
from settings import OPENAI_API_KEY

def publish_youtube_video(task):
    print("🎬 Creating automated YouTube script...")
    print("📤 Manual upload required (YouTube upload API locked).")
    print("✔ YouTube video script ready.")

    body = {
        "model": "gpt-4.1-mini",
        "input": "Write a 10 second motivational YouTube short script."
    }
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}

    resp = requests.post("https://api.openai.com/v1/responses", json=body, headers=headers)
    script = resp.json()["output"][0]["content"][0]["text"]

    print("✨ Script:", script)
    print("📤 Ready for video generation (mock)")
    print("✅ YouTube script created.")
