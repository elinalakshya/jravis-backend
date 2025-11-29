import requests
from settings import PRINTIFY_API_KEY, OPENAI_API_KEY

def publish_printify_product(task):
    print("🖨 Publishing Printify POD item... (simulation only)")
    print("✔ Printify ready for manual review.")

    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    body = {
        "model": "gpt-4.1-mini",
        "input": "Generate a unique POD t-shirt design idea related to motivation."
    }

    resp = requests.post("https://api.openai.com/v1/responses", json=body, headers=headers)
    idea = resp.json()["output"][0]["content"][0]["text"]
    print("✨ Design Idea:", idea)

    print("📤 Uploading to Printify (mock)…")
    print("✅ Printify publish complete.")
