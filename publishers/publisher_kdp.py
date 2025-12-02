import requests
from settings import OPENAI_API_KEY

def publish_kdp(task):
    print("📚 Creating KDP book outline...")
    print("📤 Manual upload to Amazon KDP required.")
    print("✔ KDP book ready.")

    body = {
        "model": "gpt-4.1",
        "input": "Create a 10-chapter outline for a personal finance book."
    }
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    resp = requests.post("https://api.openai.com/v1/responses", json=body, headers=headers)

    outline = resp.json()["output"][0]["content"][0]["text"]
    print("✨ Outline generated.")
    print("📤 KDP export (mock)")
    print("✅ KDP book outline ready.")
