import requests
from settings import OPENAI_API_KEY

def publish_affiliate_blog():
    print("📝 Creating SEO affiliate article...")

    body = {
        "model": "gpt-4.1",
        "input": "Write a 300-word SEO blog intro about trending wireless headphones."
    }
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    resp = requests.post("https://api.openai.com/v1/responses", json=body, headers=headers)

    article = resp.json()["output"][0]["content"][0]["text"]
    print("✨ Article Ready")
    print("📤 Publishing to micro-blog (mock)")
    print("✅ Affiliate blog published.")
    
