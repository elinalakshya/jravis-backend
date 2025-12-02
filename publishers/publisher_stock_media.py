import requests
from settings import OPENAI_API_KEY

def publish_stock_media(task):
    print("📸 Preparing stock media pack...")
    print("🎥 AI content generated.")
    print("📤 Manual upload required to Shutterstock/Adobe.")
    print("✔ Stock media ready.")

    prompt = {
        "model": "gpt-4.1-mini",
        "input": "Give 5 trending stock photo ideas for Shutterstock and Adobe Stock."
    }
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    resp = requests.post("https://api.openai.com/v1/responses", json=prompt, headers=headers)

    ideas = resp.json()["output"][0]["content"][0]["text"]
    print("✨ Ideas:", ideas)
    print("📤 Export ready (mock)")
    print("✅ Stock media concepts created.")
