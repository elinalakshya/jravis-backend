# src/intelligence/market_pulse.py

import os

# 🔥 Prevent Render from injecting proxies that break OpenAI client
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("http_proxy", None)
os.environ.pop("https_proxy", None)

from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")

# 🔥 Safe, correct new-SDK initialization (no proxies allowed)
client = OpenAI(api_key=api_key) if api_key else None


def get_market_pulse():
    """
    AI searches global patterns for demand spikes.
    No earnings involved — pure intelligence.
    """

    if client is None:
        return {"error": "OpenAI API key is missing"}

    prompt = """
    Identify 5 trending digital product niches for the next 30 days.
    Must be legal, ethical, global, and scalable.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message["content"]

    except Exception as e:
        return {"error": str(e)}
