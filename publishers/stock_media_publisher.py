# publishers/stock_media_publisher.py

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER", "generated")


def publish_stock_media(task):
    """
    Generates prompts for stock media creation.
    Upload manually to Shutterstock / Adobe Stock.
    """
    print("📸 Creating stock media pack...")

    try:
        prompt = """
        Generate 20 high-quality stock image prompts.
        Each prompt must include:
        - Subject
        - Style
        - Mood
        - Camera details
        - Lighting
        """

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )
        prompts = response.output_text

        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        path = f"{OUTPUT_FOLDER}/stock_media_prompts.txt"

        with open(path, "w", encoding="utf-8") as f:
            f.write(prompts)

        print("📷 Stock media prompts generated!")
        return "Stock media pack ready"

    except Exception as e:
        print("❌ Stock Media Error:", e)
        return "Stock media generation failed"
