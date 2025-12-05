# File: src/engines/newsletter_content_engine.py
from typing import Dict, Any
from src.openai_helper import openai_helper

def run_newsletter_content_engine() -> Dict[str, Any]:
    """
    Generates a full newsletter issue.
    """
    system_prompt = "You create high-engagement newsletters."

    user_prompt = (
        "Write a newsletter edition containing:\n"
        "- Subject line\n"
        "- Introduction story\n"
        "- Main lesson (detailed)\n"
        "- Practical tips (5)\n"
        "- Call to action\n"
        "Tone: friendly, smart, helpful."
    )

    result = openai_helper.generate_text(system_prompt, user_prompt)

    payload = {
        "type": "newsletter",
        "content": result
    }

    return openai_helper.format_payload("newsletter", payload)
