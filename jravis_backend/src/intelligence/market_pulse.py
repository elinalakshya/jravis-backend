# jravis_backend/src/intelligence/market_pulse.py

import os
from openai import OpenAI

def get_market_pulse():
    """
    AI searches global patterns for demand spikes.
    No earnings involved — pure intelligence.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return {"error": "OPENAI_API_KEY not set on server"}

    # Create the client INSIDE the function
    # This avoids Render injecting PROXY settings into OpenAI client creation
    client = OpenAI(api_key=api_key)

    prompt = """
    Identify 5 trending digital product niches for the next 30 days.
    Must be legal, ethical, global, and scalable.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message["content"]
