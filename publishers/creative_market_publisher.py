# publishers/creative_market_publisher.py

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER", "generated")

def publish_creative_market(task):
    """
    Generates a digital template pack for Creative Market.
    Upload must be manual because no public API exists.
    """
    print("🎨 Preparing Creative Market template bundle...")

    try:
        prompt = """
        Create a premium Canva template bundle description.
        Include:
        - Title
        - Features
        - Use cases
        - Editable elements
        - Licensing note
        """

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        text = response.output_text

        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        path = f"{OUTPUT_FOLDER}/creative_market_template.txt"

        with open(path, "w", encoding="utf-8") as f:
            f.write(text)

        print("✨ Template bundle generated (manual upload needed).")
        return "Creative Market pack ready"

    except Exception as e:
        print("❌ Creative Market Error:", e)
        return "Creative Market generation failed"
