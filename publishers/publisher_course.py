import requests
from settings import OPENAI_API_KEY

def publish_course(task):
    print("🎓 Preparing course lesson content...")
    print("✔ Course content ready for upload.")

    body = {
        "model": "gpt-4.1",
        "input": "Create a 5-module mini course on how to earn money online."
    }
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}

    resp = requests.post("https://api.openai.com/v1/responses", json=body, headers=headers)
    course = resp.json()["output"][0]["content"][0]["text"]

    print("✨ Course content ready")
    print("📤 Export course assets (mock)")
    print("✅ Course published.")
